from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from db.index import base


class Declension(base):
    __tablename__ = 'declension'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(JSON)
