from flask import Flask, render_template, _app_ctx_stack
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

from sqlalchemy.orm import scoped_session

# blueprint for auth/main routes in our app
from .auth import auth as auth_blueprint
from .main import main as main_blueprint
from .db import models
from .db.db_base import SessionLocal, engine

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():

    # create base metadata and bind to session engine
    # models.Base.metadata.create_all(bind=engine)

    # create the application object
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'jeff'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'
    db.init_app(app)
    # CORS(app)
    # app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app


# if __name__ == "__main__":
#     create_app()
