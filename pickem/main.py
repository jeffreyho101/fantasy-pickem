from datetime import datetime
from pytz import timezone, utc

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import text

from . import db
from .models import Games, Picks


main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    index: Endpoint that renders index.html

    Returns:
        str: A rendering of index.html
    """
    return render_template('index.html', current_user=current_user)


def date_inbetween(start, end):
    """
    date_inbetween: determines whether the time is currently between start and end

    Args:
        start (datetime.datetime): start time
        end (datetime.datetime): start time

    Returns:
        bool: Whether the current time is between start and end
    """
    return start <= datetime.now(timezone('US/Pacific')) <= end


def get_week():
    """
    get_week: Get the current week based on what time it currently is

    Returns:
        int: The current week of the NFL season
    """
    w2_start = datetime.strptime("15-09-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w3_start = datetime.strptime("22-09-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w4_start = datetime.strptime("29-09-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w5_start = datetime.strptime("06-10-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w6_start = datetime.strptime("13-10-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w7_start = datetime.strptime("20-10-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w8_start = datetime.strptime("27-10-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w9_start = datetime.strptime("03-11-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w10_start = datetime.strptime("10-11-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w11_start = datetime.strptime("17-11-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w12_start = datetime.strptime("24-11-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w13_start = datetime.strptime("08-12-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w14_start = datetime.strptime("15-12-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w15_start = datetime.strptime("22-12-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w16_start = datetime.strptime("29-12-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w17_start = datetime.strptime("05-12-2020", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    w17_end = datetime.strptime("12-09-2021", "%d-%m-%Y").astimezone(
        timezone('US/Pacific')
    )
    week = 0
    if datetime.now(timezone('US/Pacific')) < w2_start:
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
    elif date_inbetween(w16_start, w17_start):
        week = 16
    elif date_inbetween(w17_start, w17_end):
        week = 17
    else:
        week = 18
    return week


@main.route('/week_picks', endpoint='week_picks')
@login_required
def week_picks():
    """
    week_picks: Display a player's weekly picks on a page

    Returns:
        str: A rendering of week_picks.html with the current week and the user's current picks
    """
    # do a lookup of picks beforehand; autofill radio buttons if picks were made
    week = get_week()

    week_games = Picks.query.filter_by(week=week, user_id=current_user.id)

    games_all = week_games.order_by(
        Picks.game_date, Picks.game_time, Picks.game_id
    ).all()

    # in the event we need the df:
    # games_df = pd.read_sql(week_games.statement, week_games.session.bind)

    user_picks = (
        Picks.query.filter_by(user_id=current_user.id, week=week)
        .with_entities(Picks.pick)
        .order_by(Picks.game_date, Picks.game_time, Picks.game_id)
        .all()
    )

    up_list = [up[0] for up in user_picks]
    current_datetime = datetime.now(timezone('US/Pacific'))
    return render_template(
        'week_picks.html',
        week=week,
        name=current_user.name,
        games_sql=games_all,
        user_picks_list=up_list,
        current_datetime=current_datetime,
        datetime=datetime,
        timezone=timezone,
        astimezone=datetime.astimezone,
        utc=utc,
    )


@main.route('/week_picks', methods=['POST'])
def week_picks_post():
    """
    week_picks_post: Display a player's weekly picks on a page after processing POST request on a pick

    Returns:
        str: A rendering of week_picks.html with the current week and the user's current picks
        where the pick made by the user gets updated with a POST request
    """
    week = get_week()

    option = request.form
    game_id = next(option.keys())
    selected_pick = option[game_id]

    saved_pick = Picks.query.filter_by(
        user_id=current_user.id, week=week, game_id=game_id
    ).first()

    # only rewrite to db if the pick changes
    if saved_pick is None:
        # check the current time; only create pick if submit time is before game
        flash(
            "Internal error. Contact admin for help if this is still an issue.",
            'danger',
        )
        return redirect(url_for('main.week_picks'))

    elif saved_pick.pick != selected_pick:
        submit_datetime = datetime.now(timezone('US/Pacific'))
        saved_pick_datetime = saved_pick.game_date + ' ' + saved_pick.game_time
        game_datetime = datetime.strptime(
            saved_pick_datetime, '%Y-%m-%d %H:%M'
        ).astimezone(timezone('US/Pacific'))
        if submit_datetime >= game_datetime:
            flash(
                f"Didn't save pick change for {saved_pick.road_team} vs. {saved_pick.home_team} because the game has already started",
                'danger',
            )
            return redirect(url_for('main.week_picks'))
        else:
            saved_pick.pick = selected_pick
            db.session.commit()

    week_games = Picks.query.filter_by(week=week, user_id=current_user.id)
    games_all = week_games.order_by(
        Picks.game_date, Picks.game_time, Picks.game_id
    ).all()

    # do a lookup of picks beforehand; autofill radio buttons if picks were made
    user_picks = (
        Picks.query.filter_by(user_id=current_user.id, week=week)
        .with_entities(Picks.pick)
        .order_by(Picks.game_date, Picks.game_time, Picks.game_id)
        .all()
    )
    up_list = [up[0] for up in user_picks]

    current_datetime = datetime.now(timezone('US/Pacific'))
    return render_template(
        'week_picks.html',
        week=week,
        name=current_user.name,
        games_sql=games_all,
        user_picks_list=up_list,
        current_datetime=current_datetime,
        datetime=datetime,
        timezone=timezone,
        astimezone=datetime.astimezone,
        utc=utc,
    )


@main.route('/standings', endpoint='standings')
@login_required
def standings():
    """
    standings: Display the overall league standings

    Returns:
        str: A rendering of standings.html with the current standings in desc. order of wins
    """
    total_games = len(
        Picks.query.filter(Picks.winner != None)
        .with_entities(Picks.game_id)
        .distinct()
        .all()
    )

    # query standings directly from sqlite, output in list format to read into html
    overall_standings_query = text(
        f"select name, count(*), {total_games}-count(*) from picks where winner not null  and winner = pick group by user_id order by count(*) desc"
    )
    result = db.engine.execute(overall_standings_query)
    records = [r for r in result]

    return render_template(
        'standings.html',
        standings=records,
        datetime=datetime,
        timezone=timezone,
        astimezone=datetime.astimezone,
        utc=utc,
    )

