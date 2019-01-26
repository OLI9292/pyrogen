from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from db.index import base


class WordMorpheme(base):
    __tablename__ = 'word_morpheme'

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id'))
    morpheme_id = Column(Integer, ForeignKey('morpheme.id'))
    index = Column(Integer)
