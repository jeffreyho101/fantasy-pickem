from . import db
from .models import Picks


def update_game_times_week_1():
    pass


def update_winners_week_1():
    ids = range(1, 17)
    winners = [
        'SF',
        'DET',
        'BAL',
        'DAL',
        'GB',
        'KC',
        'IND',
        'LV',
        'LAC',
        'NE',
        'BUF',
        'PHI',
        'PIT',
        'SEA',
        'NO',
        'TEN',
    ]
    for i in range(len(ids)):
        update_results(1, ids[i], winners[i])


def update_results(week, game_id, winner):

    game_picks = Picks.query.filter_by(week=week, game_id=game_id)
    for pick in game_picks:
        pick.winner = winner
    db.session.commit()
