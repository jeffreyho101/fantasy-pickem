from flask import Flask, render_template, _app_ctx_stack
from flask_sqlalchemy import SQLAlchemy

# from flask_cors import CORS

# from sqlalchemy.orm import scoped_session

# from .db import models
# from .db.db_base import SessionLocal, engine


db = SQLAlchemy()


def create_app():

    # create base metadata and bind to session engine
    # models.Base.metadata.create_all(bind=engine)

    # create the application object
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'jeff'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    # CORS(app)
    # app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    # import auth, main and register blueprints
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app


# if __name__ == "__main__":
#     create_app()
