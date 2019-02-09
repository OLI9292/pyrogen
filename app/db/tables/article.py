from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSON

from db.index import base


class Article(base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    data = Column(JSON)
