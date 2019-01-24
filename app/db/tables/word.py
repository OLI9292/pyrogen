from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

from db.index import base


class Word(base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    grammar = Column(Enum("noun", "verb", "adjective", name="GrammarTypes"))


word_mocks = {
    "english": [
        (Word(value="carnivore", grammar="noun"), ["carn", "vor"])
    ],
    "latin": []
}
