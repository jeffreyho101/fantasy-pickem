from datetime import datetime

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import pandas as pd

from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', current_user=current_user)


@main.route('/profile', endpoint='profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


def date_inbetween(start, end):
    return start <= datetime.now() <= end


def get_week():
    w2_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w3_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w4_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w5_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w6_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w7_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w8_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w9_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w10_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w11_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w12_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w13_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w14_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w15_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w16_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    w17_start = datetime.strptime("14-09-2020", "%d-%m-%Y")
    week = 0
    if datetime.now() < w2_start:
        week = 1
    elif date_inbetween(w2_start, w3_start):
        week = 2
    elif date_inbetween(w3_start, w4_start):
        week = 3
    elif date_inbetween(w4_start, w5_start):
        week = 4
    elif date_inbetween(w5_start, w6_start):
        week = 5
    elif date_inbetween(w6_start, w7_start):
        week = 6
    elif date_inbetween(w7_start, w8_start):
        week = 7
    elif date_inbetween(w8_start, w9_start):
        week = 8
    elif date_inbetween(w9_start, w10_start):
        week = 9
    elif date_inbetween(w10_start, w11_start):
        week = 10
    elif date_inbetween(w11_start, w12_start):
        week = 11
    elif date_inbetween(w12_start, w13_start):
        week = 12
    elif date_inbetween(w13_start, w14_start):
        week = 13
    elif date_inbetween(w14_start, w15_start):
        week = 14
    elif date_inbetween(w15_start, w16_start):
        week = 15
    elif date_inbetween(w6_start, w17_start):
        week = 16
    else:
        week = 17

    return week


@main.route('/week_picks', endpoint='week_picks')
@login_required
def week_picks():
    # do a lookup of picks beforehand; autofill radio buttons if picks were made

    week = get_week()
    from .models import Games

    week_games = Games.query.filter_by(week=week)

    games_all = week_games.all()
    # in the event we need the df:
    games_df = pd.read_sql(week_games.statement, week_games.session.bind)

    from .models import Picks

    user_picks = (
        Picks.query.filter_by(user_id=current_user.id, week=week)
        .with_entities(Picks.pick)
        .all()
    )
    up_list = [up[0] for up in user_picks]

    return render_template(
        'week_picks.html', week=week, games_sql=games_all, user_picks_list=up_list
    )


@main.route('/week_picks', methods=['POST'])
def week_picks_post():

    # TODO: MAKE FORM READ-ONLY AFTER DEADLINE

    week = get_week()
    from .models import Picks

    option = request.form
    game_id = next(option.keys())
    selected_pick = option[game_id]

    saved_pick = Picks.query.filter_by(
        user_id=current_user.id, week=week, game_id=game_id
    ).first()
    # only rewrite to db if the pick changes
    if saved_pick is None:
        new_pick = Picks(
            game_id=game_id, user_id=current_user.id, week=week, pick=selected_pick
        )
        db.session.add(new_pick)
        db.session.commit()

    elif saved_pick.pick != selected_pick:
        saved_pick.pick = selected_pick
        db.session.commit()

    from .models import Games

    week_games = Games.query.filter_by(week=week)
    games_all = week_games.all()

    # do a lookup of picks beforehand; autofill radio buttons if picks were made
    user_picks = (
        Picks.query.filter_by(user_id=current_user.id, week=week)
        .with_entities(Picks.pick)
        .all()
    )
    up_list = [up[0] for up in user_picks]

    return render_template(
        'week_picks.html', week=week, games_sql=games_all, user_picks_list=up_list
    )


@main.route('/standings', endpoint='standings')
@login_required
def standings():
    return render_template('standings.html')

