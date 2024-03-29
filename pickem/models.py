from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    """ Schema for the User table """

    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    timezone = db.Column(db.String(1000))


class Picks(UserMixin, db.Model):
    """ Schema for the Picks table """

    id = db.Column(db.Integer, primary_key=True)  # id is useless in this table
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    week = db.Column(db.Integer)
    game_id = db.Column(db.Integer)
    game_date = db.Column(db.String(100))
    game_time = db.Column(db.String(100))
    road_team = db.Column(db.String(100))
    home_team = db.Column(db.String(100))
    # pick: team initial of the pick they make
    pick = db.Column(db.String(100))
    # winner: team initial of the winner of the game (added later)
    # if game ends in tie, winner = 'TIE'
    winner = db.Column(db.String(100))


class Games2021(UserMixin, db.Model):
    """ Schema for the Games table """

    game_id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    week = db.Column(db.Integer)
    visitor_fullname = db.Column(db.String(100))
    road_pts = db.Column(db.Integer)
    home_fullname = db.Column(db.String(100))
    home_pts = db.Column(db.Integer)
    road_team = db.Column(db.String(100))
    home_team = db.Column(db.String(100))
    game_date = db.Column(db.String(10))
    game_time_pst = db.Column(db.String(10))
    final = db.Column(db.Boolean)


# class Games(UserMixin, db.Model):
#     """
#     DEPRECATED (from 2020 db).
#
#     Schema for the Games table
#     """

#     game_id = db.Column(
#         db.Integer, primary_key=True
#     )  # primary keys are required by SQLAlchemy
#     week = db.Column(db.Integer)
#     road_team = db.Column(db.String(100))
#     home_team = db.Column(db.String(100))
#     # game_date: of format "YYYY-MM-DD"
#     game_date = db.Column(db.String(10))
#     game_time = db.Column(db.String(10))
#     road_pts = db.Column(db.Integer)
#     home_pts = db.Column(db.Integer)
#     final = db.Column(db.Boolean)
#     # winner: team initial of the winner of the game (added later)
#     winner = db.Column(db.String(100))

