from datetime import datetime, timedelta
from pytz import timezone, utc
import time

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import text

from . import db
from .models import Games, Picks, User


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


def display_week(now=datetime.now()):
    """
    get_week: Get the current week based on what time it currently is.
              Assume that pickem weeks start on Wednesday.

    Returns:
        int: The current week of the NFL season
    """
    w1_start = datetime.strptime("2021-09-08", "%Y-%m-%d")
    week = 1
    while week < 18:
        if now - timedelta(days=7) < w1_start:
            break
        week += 1
        now -= timedelta(days=7)
    return week


@main.route('/week_picks', endpoint='week_picks')
@login_required
def week_picks(week=display_week()):
    """
    week_picks: Display a player's weekly picks on a page

    Returns:
        str: A rendering of week_picks.html with the current week and the user's current picks
    """
    # do a lookup of picks beforehand; autofill radio buttons if picks were made
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
        current_username=current_user.name,
        name=current_user.name,
        user_timezone=current_user.timezone,
        games_sql=games_all,
        user_picks_list=up_list,
        current_datetime=current_datetime,
        datetime=datetime,
        timezone=timezone,
        astimezone=datetime.astimezone,
        utc=utc,
        week_list=list(range(1, 18)),
        user_list=[u[0] for u in User.query.with_entities(User.name).all()],
    )


@main.route('/week_picks', methods=['POST'])
@login_required
def week_picks_post(week=display_week()):
    """
    week_picks_post: Display a player's weekly picks on a page after processing POST request on a pick

    Returns:
        str: A rendering of week_picks.html with the current week and the user's current picks
        where the pick made by the user gets updated with a POST request
    """
    display_name = current_user.name
    user_id = current_user.id
    if 'week_display' in request.form:
        week = int(request.form['week_display'])
    if 'user_display' in request.form:
        display_name = request.form['user_display']
        user_id = (
            User.query.filter_by(name=display_name).with_entities(User.id).first()[0]
        )
    else:
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
            game_datetime = timezone('US/Pacific').localize(
                datetime.strptime(saved_pick_datetime, '%Y-%m-%d %H:%M')
            )
            if submit_datetime >= game_datetime:
                flash(
                    f"Didn't save pick change for {saved_pick.road_team} vs. {saved_pick.home_team} because the game has already started",
                    'danger',
                )
                return redirect(url_for('main.week_picks'))
            else:
                update_text = text(
                    f"update picks set pick = '{selected_pick}' where user_id = {user_id} and game_id = {game_id}"
                )
                db.engine.execute(update_text)
                db.session.commit()

    week_games = Picks.query.filter_by(week=week, user_id=user_id)
    games_all = week_games.order_by(
        Picks.game_date, Picks.game_time, Picks.game_id
    ).all()
    # do a lookup of picks beforehand; autofill radio buttons if picks were made
    user_picks = (
        Picks.query.filter_by(user_id=user_id, week=week)
        .with_entities(Picks.pick)
        .order_by(Picks.game_date, Picks.game_time, Picks.game_id)
        .all()
    )
    up_list = [up[0] for up in user_picks]

    current_datetime = datetime.now(timezone('US/Pacific'))
    return render_template(
        'week_picks.html',
        week=week,
        current_username=current_user.name,
        name=display_name,
        user_timezone=current_user.timezone,
        games_sql=games_all,
        user_picks_list=up_list,
        current_datetime=current_datetime,
        datetime=datetime,
        timezone=timezone,
        astimezone=datetime.astimezone,
        utc=utc,
        week_list=list(range(1, 18)),
        user_list=[u[0] for u in User.query.with_entities(User.name).all()],
    )


@main.route('/picks_breakdown')
@login_required
def picks_breakdown(week=display_week()):
    """
    picks_breakdown: Display a page allowing for a more detailed breakdown of picks

    Returns:
        str: A rendering of picks_breakdown.html with default pick breakdown for the given week
    """
    current_datetime = datetime.now(timezone('US/Pacific'))
    return render_template('picks_breakdown.html', week=week,)


@main.route('/picks_breakdown', methods=['POST'])
@login_required
def picks_breakdown_post(week=display_week()):
    """
    picks_breakdown: Display a player's weekly picks on a page after processing POST request on a pick

    Returns:
        str: A rendering of picks_breakdown.html with parameters that are updated with a POST request
    """
    current_datetime = datetime.now(timezone('US/Pacific'))
    return render_template('picks_breakdown.html', week=week,)


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
    # records: [user, ovr_w, ovr_l, tw_w, tw_l, lw_w, lw_l,]
    records = []
    if total_games == 0:
        from .models import User

        users = User.query.with_entities(User.name).all()
        records = [(r[0], 0, 0, 0, 0, 0, 0) for r in users]
    else:
        week = display_week()
        # query standings directly from sqlite, output in list format to read into html
        overall_standings_query = text(
            f"select name, sum(pick = winner) as correct, sum(pick != winner) as incorrect, sum(pick = winner and week = {week}) as this_week_correct, sum(pick != winner and week = {week}) as this_week_incorrect, sum(pick = winner and week = {week-1}) as last_week_correct, sum(pick != winner and week = {week-1}) as last_week_incorrect from picks where winner not null group by name order by correct desc;"
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


@main.route('/settings', endpoint='settings')
@login_required
def settings():
    """
    settings: Display configurable user settings

    Returns:
        str: A rendering of settings.html with the current standings in desc. order of wins
    """
    display_name = current_user.name
    user_timezone = current_user.timezone
    timezones = [
        "Europe/Berlin",
        "US/Alaska",
        "US/Arizona",
        "US/Central",
        "US/Eastern",
        "US/Mountain",
        "US/Pacific",
        "UTC",
    ]
    return render_template(
        'settings.html',
        timezones=timezones,
        display_name=display_name,
        user_timezone=user_timezone,
    )


@main.route('/settings', methods=['POST'])
@login_required
def settings_post():
    """
    settings_post: Send POST request of configurable settings

    Returns:
        str: A rendering of settings.html with the current standings in desc. order of wins
    """
    new_display_name = request.form.get('display_name')
    if new_display_name == "":
        new_display_name = current_user.name
    valid_name = len(new_display_name) <= 20
    if not valid_name:
        flash("Name is invalid. Must be between 1 and 20 characters", 'danger')
        return redirect(url_for('main.settings'))

    new_timezone = request.form.get('timezone')

    from .models import User

    picks_update = text(
        f"update picks set name = '{new_display_name}' where name = '{current_user.name}'"
    )
    db.engine.execute(picks_update)

    user = User.query.get(current_user.id)
    user.timezone = new_timezone
    user.name = new_display_name
    db.session.commit()

    timezones = [
        "Europe/Berlin",
        "US/Alaska",
        "US/Arizona",
        "US/Central",
        "US/Eastern",
        "US/Mountain",
        "US/Pacific",
        "UTC",
    ]

    flash("Successfully changed user settings.", 'success')
    return render_template(
        'settings.html',
        timezones=timezones,
        display_name=new_display_name,
        user_timezone=new_timezone,
    )
