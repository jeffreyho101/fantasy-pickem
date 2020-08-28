from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Picks(UserMixin, db.Model):
    game_id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    pick = db.Column(db.String(100))


class Games(UserMixin, db.Model):
    game_id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    week = db.Column(db.Integer)
    road_team = db.Column(db.String(100))
    home_team = db.Column(db.String(100))
    road_pts = db.Column(db.Integer)
    home_pts = db.Column(db.Integer)
    final = db.Column(db.Boolean)
    winner = db.Column(db.String(100))
