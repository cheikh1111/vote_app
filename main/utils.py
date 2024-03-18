from cryptography.fernet import Fernet
from .models import User, Vote
from flask import session, request
from . import db

cipher_suite = Fernet(Fernet.generate_key())
candidates = ["UGEM", "UNEM", "SNEM", "ANEM", "N"]


def encrypt(string: str) -> str:
    return cipher_suite.encrypt(string.encode()).decode()


def decrypt(string: str) -> str:
    return cipher_suite.decrypt(string.encode()).decode()


def encrypt_cookie(cookie: str):
    key = b"n9Q-bYxtQG_UTbBZ2klFCr6K_feqXZJ9IqraPVEU4Tc="
    fernet = Fernet(key)
    return fernet.encrypt(cookie.encode()).decode()


def decrypt_cookie(cookie: str):
    key = b"n9Q-bYxtQG_UTbBZ2klFCr6K_feqXZJ9IqraPVEU4Tc="
    fernet = Fernet(key)
    return fernet.decrypt(cookie.encode()).decode()


def get_votes_percentage():
    votes = Vote.query.all()

    if not votes:
        return 0, 0, 0, 0, 0, 0

    get_percentage = (
        lambda name: len([vote for vote in votes if vote.voted_for == name])
        / total
        * 100
    )
    total = len(votes)
    ugem_percentage = get_percentage("UGEM")
    unem_percentage = get_percentage("UNEM")
    snem_percentage = get_percentage("SNEM")
    anem_percentage = get_percentage("ANEM")
    neutre_percentage = get_percentage("N")

    return (
        total,
        ugem_percentage,
        unem_percentage,
        snem_percentage,
        anem_percentage,
        neutre_percentage,
    )


def add_voice(
    voted_for: str, user_id: int
) -> bool:  # returns boolean indicating success or failure
    user = User.query.get(user_id)
    if not user.voted and voted_for in candidates:
        vote = Vote(voted_for=voted_for, user_id=user_id)
        user.voted = True
        db.session.add(vote)
        db.session.commit()
        db.session.close()
        return True

    return False


def user_exists(registration_num):
    user = User.query.filter_by(registration_num=registration_num).first()

    return user and True


def is_logged_in():
    user_id = session.get("user_id", None)
    user_id_cookie = request.cookies.get("user_id", None)
    if user_id:
        user_id = int(decrypt(user_id))
        user = User.query.get(user_id_cookie)
        return user if getattr(user, "id", False) else False

    elif user_id_cookie:
        user_id_cookie = int(decrypt_cookie(user_id_cookie))
        user = User.query.get(user_id_cookie)
        return user if getattr(user, "id", False) else False
    return False
