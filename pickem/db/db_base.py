from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# define path to database, engine, and Base db class
SQLALCHEMY_DB_URL = "sqlite:///db/test.db"
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create Base metaclass for the db
# declarative_base() allows you to write just one model per table that app uses
# That model is then used in Python outside of the app and in the database.
Base = declarative_base()
