from . import db
from datetime import datetime, UTC

get_utc_time = lambda: datetime.now(UTC)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    registration_num = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    voted = db.Column(db.Boolean, default=False)
    vote = db.relationship("Vote", backref="user", lazy=True)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=get_utc_time)
    voted_for = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
