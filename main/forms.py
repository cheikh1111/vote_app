from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import Length, InputRequired


class RegisterForm(FlaskForm):
    name = StringField(
        "Nom Complet",
        [
            InputRequired("Saisie requise"),
            Length(
                min=4, message="Minimum Longueure pour un nom complet est 5 lettres"
            ),
        ],
        render_kw={"placeholder": "Nom complet"},
    )
    registration_num = StringField(
        "Entrer votre Matricule",
        [
            InputRequired("Saisie requise"),
            Length(min=5, max=6),
        ],
        render_kw={"placeholder": "Matricule"},
    )

    password = PasswordField(
        "Mot de passe",
        [
            InputRequired("Saisie requise"),
            Length(min=7, message="la longueur minimum du mot de pass est 7 lettres"),
        ],
        render_kw={"placeholder": "Password"},
    )
    password_c = PasswordField(
        "Confirmer vos mot de passe",
        [
            InputRequired(""),
            Length(min=7, message="la longueur minimum du mot de pass est 7 lettres"),
        ],
        render_kw={"placeholder": "Password Confirm"},
    )

    submit = SubmitField("S'inscrir")


class LoginForm(FlaskForm):
    registration_num = StringField(
        "Matricule",
        [
            InputRequired("Saisie requise"),
            Length(min=5, max=6),
        ],
        render_kw={"placeholder": "Matricule"},
    )

    password = PasswordField(
        "Mot de passe",
        [InputRequired("Saisie requise")],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Se connectez")


class VoteForm(FlaskForm):
    choices = (
        ("UGEM", "UGEM"),
        ("UNEM", "UNEM"),
        ("SNEM", "SNEM"),
        ("ANEM", "ANEM"),
        ("N", "Neutre"),
    )
    radio_field = RadioField("Votez", choices=choices)
    submit = SubmitField("Votez")
