import json

from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from db.index import base, session


class DictionaryModel(base):
    __tablename__ = 'dictionary'

    id = Column(String, primary_key=True)
    data = Column(JSON)

    language_id = Column(Integer, ForeignKey('language.id'))


class Dictionary(SQLAlchemyObjectType):
    class Meta:
        model = DictionaryModel
        only_fields = ("id", "data", "language_id")


class CreateDictionary(graphene.Mutation):
    class Arguments:
        json_string = graphene.String(required=True)
        language_id = graphene.Int(required=True)

    dictionary = graphene.Field(lambda: Dictionary)

    def mutate(self, info, json_string, language_id):
        try:
            data = json.loads(json_string)
            dictionary = DictionaryModel(data=data, language_id=language_id)
            session.add(dictionary)
            session.commit()
            return CreateDictionary(dictionary=dictionary)
        except Exception as error:
            print "ERR:", error
            return {"error": error}


def resolve_dictionaries(self, info):
    try:
        results = session.query(DictionaryModel).all()
        return results
    except Exception as error:
        print "ERR:", error
        return {"error": error}
