from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import os

db = SQLAlchemy()


def create_app() -> Flask:

    app = Flask(__name__)
    app.secret_key = secrets.token_hex(18)
    DB_URI = os.getenv("DB_URI", None)
    if not DB_URI:
        print("\033[32m[INFO]  Programmed by Cheikhsidiya med.\033[0m")
        print(
            "\033[31m[ERROR] You forgot to add the DB_URI environment variable\033[0m"
        )
        quit()
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFCATIONS"] = False
    db.init_app(app)
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    from .models import User, Vote

    return app


app = create_app()

with app.app_context():
    db.create_all()
