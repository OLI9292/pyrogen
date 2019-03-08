import json

from sqlalchemy import Column, String, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, ARRAY

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from ..join_tables.word_morpheme import WordMorphemeModel, WordMorpheme
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
    definition = Column(String)
    # TODO: - able to click off highlighting blacklist_highlight = Column(Array(Integer))

    noun_attributes = Column(ARRAY(String))
    blacklist = Column(ARRAY(String))

    grammar = Column(Enum(
        "noun",
        "verb",
        "adjective",
        "copula",
        "article",
        name="GrammarTypes"))

    curriculum_id = Column(String)

    language_id = Column(Integer, ForeignKey('language.id'))
    dictionary_id = Column(String, ForeignKey('dictionary.id'))
    dictionary = relationship('DictionaryModel')

    english_morpheme_id = Column(Integer, ForeignKey('morpheme.id'))
    english_morpheme = relationship('MorphemeModel')

    template_id = Column(String)
    properties = Column(JSON, default='[]')


def resolve_word(self, info, id):
    try:
        return session.query(MorphemeModel).get(id)
    except Exception as error:
        print("ERR:", error)
        return {"error": error}


def get_word_morphemes(word):
    morphemes = []
    relationships = session.query(WordMorphemeModel).filter(
        WordMorphemeModel.word_id == word.id).all()
    for relationship in relationships:
        morpheme = session.query(MorphemeModel).get(
            relationship.morpheme_id)
        morphemes.append(Derivation(
            relationship=relationship, morpheme=morpheme))
    return WordAndMorpheme(word=word, morphemes=morphemes)


def resolve_word(self, info, id):
    word = session.query(MorphemeModel).get(id)
    return get_word_morphemes(word)


def resolve_words(self, info, curriculum_id):
    words = session.query(MorphemeModel).filter(
        MorphemeModel.curriculum_id == curriculum_id).all()
    return [get_word_morphemes(word) for word in words]


class Morpheme(SQLAlchemyObjectType):
    class Meta:
        model = MorphemeModel
        only_fields = (
            "id",
            "value",
            "animacy",
            "free",
            "definition",
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
            "curriculum_id",
            "english_morpheme_id",
            "template_id",
            "properties",
        )


class Derivation(graphene.ObjectType):
    relationship = graphene.Field(WordMorpheme)
    morpheme = graphene.Field(Morpheme)


class WordAndMorpheme(graphene.ObjectType):
    word = graphene.Field(Morpheme)
    morphemes = graphene.List(Derivation)


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
        definition = graphene.String(required=False)
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
                definition=kwargs.get("definition", None),
                noun_attributes=kwargs.get("noun_attributes", None),
                blacklist=kwargs.get("blacklist", None),
                person=kwargs.get("person", None),
                transitive=kwargs.get("transitive", None),
                intransitive=kwargs.get("intransitive", None),
                dictionary_id=kwargs.get("dictionary_id", None),
                curriculum_id=kwargs.get("curriculum_id", None),
                template_id=kwargs.get("template_id", None),
                properties=kwargs.get("properties", None),
            )

            session.add(morpheme)
            session.commit()
            return CreateMorpheme(morpheme=morpheme)
        except Exception as error:
            print("ERR:", error)
            return {"error": error}
