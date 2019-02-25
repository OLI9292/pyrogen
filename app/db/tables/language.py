import json

from sqlalchemy import Column, String, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSON

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from db.index import base, session


class LanguageModel(base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Language(SQLAlchemyObjectType):
    class Meta:
        model = LanguageModel
        only_fields = ("id", "name")


class CreateLanguage(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    language = graphene.Field(lambda: Language)
    id = graphene.Field(graphene.String, to=graphene.String())

    def mutate(self, info, name):
        try:
            Language = LanguageModel(name=name)
            session.add(Language)
            session.commit()
            return CreateLanguage(Language=Language)
        except Exception as error:
            print("ERR:", error)
            return {"error": error}


def resolve_languages(self, info):
    try:
        results = session.query(LanguageModel).all()
        return results
    except Exception as error:
        print("ERR:", error)
        return {"error": error}
