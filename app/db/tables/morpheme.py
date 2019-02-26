import json

from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app.db.join_tables.word_morpheme import WordMorphemeModel
from app.db.index import base, session


class MorphemeModel(base):
    __tablename__ = 'morpheme'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    animacy = Column(Integer)
    free = Column(Boolean, default=True)
    copula = Column(Boolean, default=False)
    person = Column(Integer)
    transitive = Column(Boolean, default=False)
    intransitive = Column(Boolean, default=False)
    irregular = Column(JSON)
    grammar = Column(Enum("noun", "verb", "adjective", name="GrammarTypes"))

    language_id = Column(Integer, ForeignKey('language.id'))
    dictionary_id = Column(String, ForeignKey('dictionary.id'))
    dictionary = relationship('DictionaryModel')


def resolve_word(self, info, id):
    try:
        word = session.query(MorphemeModel).get(id)
        return word
    except Exception as error:
        print("ERR:", error)
        return {"error": error}


class Morpheme(SQLAlchemyObjectType):
    class Meta:
        model = MorphemeModel
        only_fields = (
            "id",
            "value",
            "animacy",
            "free",
            "copula",
            "person",
            "transitive",
            "intransitive",
            "irregular",
            "grammar",
            "language_id",
            "language",
            "dictionary_id",
            "derived_from"
        )


def resolve_morphemes(self, info):
    try:
        results = session.query(MorphemeModel).all()
        return results
    except Exception as error:
        print("ERR:", error)
        return {"error": error}


class CreateMorpheme(graphene.Mutation):
    class Arguments:
        grammar = graphene.String(required=True)
        language_id = graphene.Int(required=True)
        value = graphene.String(required=False)
        animacy = graphene.Int(required=False)
        free = graphene.Boolean(required=False)
        copula = graphene.Boolean(required=False)
        person = graphene.Int(required=False)
        transitive = graphene.Boolean(required=False)
        intransitive = graphene.Boolean(required=False)
        irregular = graphene.String(required=False)

    morpheme = graphene.Field(lambda: Morpheme)

    def mutate(self, info, grammar, language_id, **kwargs):
        try:
            irregular = kwargs.get("irregular", None)
            if irregular != None:
                irregular = json.loads(irregular)

            morpheme = MorphemeModel(
                grammar=grammar,
                language_id=language_id,
                irregular=irregular,
                value=kwargs.get("value", None),
                animacy=kwargs.get("animacy", None),
                free=kwargs.get("free", None),
                copula=kwargs.get("copula", None),
                person=kwargs.get("person", None),
                transitive=kwargs.get("transitive", None),
                intransitive=kwargs.get("intransitive", None),
                dictionary_id=kwargs.get("dictionary_id", None),
            )

            session.add(morpheme)
            session.commit()
            return CreateMorpheme(morpheme=morpheme)
        except Exception as error:
            print("ERR:", error)
            return {"error": error}
