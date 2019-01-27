from sqlalchemy import Column, String, Enum, Boolean, Integer

from db.index import base


class Word(base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    grammar = Column(Enum("noun", "verb", "adjective", name="GrammarTypes"))
