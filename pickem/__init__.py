from bs4 import BeautifulSoup
from flask import Flask, render_template, _app_ctx_stack
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests

# from flask_cors import CORS

# from sqlalchemy.orm import scoped_session

# from .db import models
# from .db.db_base import SessionLocal, engine


db = SQLAlchemy()


def db_config():
    app = Flask(__name__)
    with open("pickem/DB_SECRET_KEY", "r") as file:
        db_key = file.readline().strip()

    app.config['SECRET_KEY'] = db_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


def create_app():

    # create base metadata and bind to session engine
    # models.Base.metadata.create_all(bind=engine)

    # create the application object
    app = db_config()

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # CORS(app)
    # app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    # import auth, main and register blueprints
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app


def init_schedule_locally():
    return pd.read_csv('pickem/static/files/matchups_2020.csv')


def init_schedule_espn():
    # scrape schedule table from ESPN
    res = requests.get("http://www.espn.com/nfl/schedulegrid")
    soup = BeautifulSoup(res.content, 'lxml')
    table = soup.find_all('table')[0]
    sched_grid = pd.read_html(str(table))[0]
    # the column names are listed in row 1; remove first two rows from table after that
    sched_grid.columns = sched_grid.iloc[1]
    sched_grid = (
        sched_grid.iloc[2:].rename_axis(None, axis=1).set_index('TEAM', drop=True)
    )
    sched_list_cols = ['week', 'road_team', 'home_team']
    sched_list = pd.DataFrame(columns=sched_list_cols)
    for week in sched_grid.columns:
        matchup = (
            sched_grid[week]
            .loc[sched_grid[week].str.startswith('@', na=False)]
            .reset_index()
        )
        matchup = matchup.set_index(pd.Index([int(week)] * len(matchup))).reset_index()
        matchup[week] = matchup[week].map(lambda x: x.lstrip('@'))
        matchup.columns = sched_list_cols
        sched_list = sched_list.append(matchup)
    sched_list = sched_list.reset_index()
    sched_list['road_pts'] = 0
    sched_list['home_pts'] = 0
    sched_list['final'] = False
    sched_list['winner'] = ''
    # sched_list['game_id'] = sched_list.index
    sched_list = sched_list.drop(columns=['index'])

    return sched_list


def init_schedule():
    sched_list = init_schedule_locally()
    from .models import Games

    app = db_config()
    db.init_app(app)
    with app.app_context():
        for index, row in sched_list.iterrows():
            game_add = Games(
                week=row['week'],
                road_team=row['road_team'],
                home_team=row['home_team'],
                game_date='2099-05-01',
                game_time='23:59',
                road_pts=0,
                home_pts=0,
                final=False,
                winner='',
            )
            db.session.add(game_add)
            db.session.commit()
