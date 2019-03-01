import json

from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, ARRAY

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from ..join_tables.word_morpheme import WordMorphemeModel
from ..index import base, session


class MorphemeModel(base):
    __tablename__ = 'morpheme'

    id = Column(Integer, primary_key=True)
    value = Column(String)

    free = Column(Boolean, default=True)
    person = Column(Integer)
    animacy = Column(Integer)  # move to noun attributes
    transitive = Column(Boolean, default=False)  # move to verb attributes
    intransitive = Column(Boolean, default=False)  # move to verb attributes

    irregular = Column(JSON)

    noun_attributes = Column(ARRAY(String))
    blacklist = Column(ARRAY(String))

    grammar = Column(Enum(
        "noun",
        "verb",
        "adjective",
        "copula",
        "article",
        name="GrammarTypes"))

    language_id = Column(Integer, ForeignKey('language.id'))
    dictionary_id = Column(String, ForeignKey('dictionary.id'))
    dictionary = relationship('DictionaryModel')

    english_morpheme_id = Column(Integer, ForeignKey('morpheme.id'))
    english_morepheme = relationship('MorphemeModel')


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
            "person",
            "transitive",
            "intransitive",
            "noun_attributes",
            "blacklist",
            "irregular",
            "grammar",
            "language_id",
            "language",
            "dictionary_id",
            "derived_from",
            "english_morpheme_id"
        )


def resolve_morphemes(self, info):
    try:
        results = session.query(MorphemeModel).all()
        print results
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
        person = graphene.Int(required=False)
        noun_attributes = graphene.List(graphene.String, required=False)
        blacklist = graphene.List(graphene.String, required=False)
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
                noun_attributes=kwargs.get("noun_attributes", None),
                blacklist=kwargs.get("blacklist", None),
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
