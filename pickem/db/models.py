from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .db_base import Base

# db class containing table columns (extends Base)
class Record(Base):
    __tablename__ = "Records"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    team1 = Column(String)
    wins = Column(Integer)
