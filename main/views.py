from .utils import (
    add_voice,
    encrypt,
    decrypt,
    decrypt_cookie,
    encrypt_cookie,
    get_votes_percentage,
    user_exists,
    is_logged_in,  # this will also return the user object if the user is logged in
)
from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    session,
    make_response,
    request,
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Vote
from .forms import VoteForm, LoginForm, RegisterForm
from . import db

views = Blueprint("views", __name__)


@views.route("/")
def home():
    form = VoteForm()
    logged_in = False
    voted = False
    user = ...
    should_set_cookie = False
    should_clear_invalid_cookie = False

    if user_id := session.get("user_id", None):
        logged_in = True
        user = User.query.get(decrypt(user_id))
        if user:
            voted = user.voted

        # this indicates redirect
        if request.url != request.host_url:
            should_set_cookie = True

    elif user_id := request.cookies.get("user_id", None):
        logged_in = True
        user = User.query.get(decrypt_cookie(user_id))
        if user:
            voted = user.voted
        else:
            logged_in = False
            should_set_cookie = True
    if not logged_in:
        flash("connectez-vous pour votez ", category="info")

    total, ugem, unem, snem, anem, neutre = get_votes_percentage()

    if voted and request.url == request.host_url:
        flash(
            f"Vous avez voté pour:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {user.vote[0].voted_for}",
            "info",
        )

    response = make_response(
        render_template(
            "home.html",
            logged=logged_in,
            voted=voted,
            total=total,
            ugem=ugem,
            unem=unem,
            snem=snem,
            anem=anem,
            neutre=neutre,
            form=form,
        )
    )

    if user_id := session.get("user_id", None) and should_set_cookie:
        user_id = encrypt_cookie(decrypt(user_id))
        response.set_cookie("user_id", user_id, max_age=2000000)

    elif should_clear_invalid_cookie:
        response.delete_cookie("user_id")
    return response


@views.route("/submit-vote", methods=["POST"])
def vote():
    form = VoteForm()
    if form.validate_on_submit():
        voted_for = form.radio_field.data

        user = is_logged_in()
        if user:
            success = add_voice(voted_for, user.id)
            if success:
                flash("Votre vote a été enregistré avec succès", "success")
                return redirect("/")
        else:
            flash("une erreur s'est produite", category="error")
            return redirect("/")
    return 401


@views.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and not is_logged_in():
        name = form.name.data
        registration_num = form.registration_num.data
        password = form.password.data
        password_c = form.password_c.data

        if registration_num and password and password == password_c:
            if not user_exists(registration_num):
                user = User(
                    name=name,
                    registration_num=registration_num,
                    password=generate_password_hash(
                        password, method="pbkdf2:sha512", salt_length=16
                    ),
                )
                db.session.add(user)
                db.session.commit()
                session["user_id"] = encrypt(str(user.id))
                response = make_response(redirect("/"))
                response.set_cookie(
                    "user_id", encrypt_cookie(str(user.id)), max_age=2000000
                )
                db.session.close()
                flash("l'opération a termine avec succès", category="success")
                return response
            else:
                flash("Le matricule est déja utiliser", category="error")
        else:
            flash("veuillez entrer des informations valides", category="error")
        return redirect("/register")
    return render_template("register.html", form=form)


@views.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit() and not is_logged_in():
        registration_num = form.registration_num.data
        password = form.password.data

        user = User.query.filter_by(registration_num=registration_num).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = encrypt(str(user.id))
            return redirect("/")
        else:
            flash("Matricule ou mot de passe incorrect", category="error")
            return redirect("/login")

    return render_template("login.html", form=form)


@views.app_errorhandler(404)
def e_404(e):
    return render_template("404.html"), 404


@views.app_errorhandler(500)
def e_500(e):
    return redirect("/")
