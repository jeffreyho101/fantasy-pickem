# Fantasy Pick-em

Constructing a web app to host a weekly pick-em style series of matchup predictions for fantasy football


- Frontend: HTML (with jinja2 templating and bits of boostrap)
- Backend: Flask
- DB: SQLite


### DB Setup:

First: to initialize a database secret key, create a file `pickem/DB_SECRET_KEY` that contains the db's secret key on the first line. On initialization, the DB_SECRET_KEY will be setup to have this as the secret key.

The database can be set up in one of two ways:

1. In the base directory, open up a repl with `python`. Then type the following:

```
from pickem import db, create_app, init_schedule
db.create_all(app=create_app())
init_schedule()
```

This creates all the tables as defined in `models.py`; `init_schedule()` scrapes the schedule data from ESPN at the start of the season and turns it into a format that is more readable before writing to the `games` table (*should only be done once total*).

2. Manually: Create the file `pickem/<name_of_db>.db` and manually add the requisite tables in (far larger hassle)
- *note: by default, this program will save the table as `pickem_tables.db` in method 1 so either use the same name or change this in `__init.py__`*


## To run:

- Ensure a FLASK_APP variable is set (ie. to the folder `pickem`). Optionally, flip the `FLASK_DEBUG` flag if you want debug mode to be on.
```
export FLASK_APP=pickem
export FLASK_DEBUG=1
```
- Run flask app from the root directory:
```
flask run
```
OR
- Run flask app with `run.py` out of the root directory:
```
python run.py
```

## Backporting old user data and populating the picks table

- Copy the user table to the new db
- wipe picks table (optional)
- re-add to picks table based on user

By script:
```
sqlite3 pickem/<old db name> ".dump user" | sqlite3 pickem/<new db name>.db
python backport.py
```