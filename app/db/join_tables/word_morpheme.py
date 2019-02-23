from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from db.index import base


class WordMorphemeModel(base):
    __tablename__ = 'word_morpheme'

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('morpheme.id'))
    morpheme_id = Column(Integer, ForeignKey('morpheme.id'))
    value = Column(String)
    start_index = Column(Integer)


class WordMorpheme(SQLAlchemyObjectType):
    class Meta:
        model = WordMorphemeModel
        only_fields = ("id", "word_id", "morpheme_id", "value", "start_index")
