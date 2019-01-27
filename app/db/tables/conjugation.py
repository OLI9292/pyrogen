from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSON

from db.index import base


class Conjugation(base):
    __tablename__ = 'conjugation'

    id = Column(Integer, primary_key=True)
    data = Column(JSON)
