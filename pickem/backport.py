import os
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pickem.models import User, Games2021, Picks


def copy_old_table(old_name, new_name):
    os.system(f'sqlite3 pickem/{old_name} ".dump user" | sqlite3 pickem/{new_name}.db')


def port_old_users(clear_table=False):
    # define path to database, engine, and Base db class
    SQLALCHEMY_DB_URL = "sqlite:///pickem/pickem_tables_2021.db"
    engine = create_engine(SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    SessionLocal.configure(bind=engine)
    session = SessionLocal()

    Base = declarative_base()

    # Clear the picks table if requested.
    if clear_table:
        clear_query = text(f"delete from picks;")
        cq = engine.execute(clear_query)

    query = text(f"select * from user;")
    result = engine.execute(query)

    # add back to the picks table if the user doesn't already have picks
    for r in result.fetchall():
        query_existing_user = text(
            f"select * from picks where user_id = {r['id']} limit 1;"
        )
        existing_user_results = engine.execute(query_existing_user)
        # if there are results alraedy in the picks table,
        if existing_user_results.fetchall():
            print(f"Not adding picks for {r.name} - picks already exist in the table.")
            continue

        # add schedule with all blank picks for new user into Picks table
        games_query = text(f"select * from games2021;")
        games_result = engine.execute(games_query)

        for game in games_result.fetchall():
            new_empty_pick = Picks(
                user_id=r.id,
                name=r.name,
                week=game.week,
                game_id=game.game_id,
                game_date=game.game_date,
                game_time=game.game_time_pst,
                road_team=game.road_team,
                home_team=game.home_team,
                pick='',
            )
            # add row to table
            session.add(new_empty_pick)

    # commit changes - add empty picks
    session.commit()
    return


if __name__ == '__main__':
    port_old_users(False)

