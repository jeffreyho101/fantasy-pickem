# Fantasy Pick-em

Constructing a web app to host a weekly pick-em style series of matchup predictions for fantasy football


- Frontend: HTML (with bits off css/js/boostrap)
- Backend: Flask
- DB: SQLite


### DB Setup:

The database can be set up in one of two ways:

1. In the base directory, open up a repl with `python`. Then type the following:

```
from pickem import db, create_app
db.create_all(app=create_app())
```

2. Manually: Create the file `pickem/<name_of_db>.db` and manually add the requisite tables in



## To run:

- Ensure a FLASK_APP variable is set (ie. to the folder `pickem`):
```
export FLASK_APP=pickem
```
- Run flask app from the root directory: `flask run`
