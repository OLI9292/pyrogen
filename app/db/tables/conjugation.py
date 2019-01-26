from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from db.index import base


class Conjugation(base):
    __tablename__ = 'conjugation'

    id = Column(Integer, primary_key=True)
    data = Column(JSON)


conjugation_mocks = {
    "english": [],
    "latin": []
}
