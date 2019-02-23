import json
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

import graphene
from flask_graphql import GraphQLView
from graphql import GraphQLError

from db.seed import seed_db, session
from db.tables.dictionary import DictionaryModel, Dictionary, CreateDictionary, resolve_dictionaries
from db.tables.morpheme import MorphemeModel, Morpheme, CreateMorpheme, resolve_morphemes, resolve_word
from db.tables.language import LanguageModel, Language, CreateLanguage, resolve_languages
from db.join_tables.word_morpheme import WordMorphemeModel, WordMorpheme
from game.index import create_clause


class Derivation(graphene.ObjectType):
    relationship = graphene.Field(WordMorpheme)
    morpheme = graphene.Field(Morpheme)


class Query(graphene.ObjectType):
    dictionaries = graphene.List(Dictionary, resolver=resolve_dictionaries)

    morphemes = graphene.List(Morpheme, resolver=resolve_morphemes)

    languages = graphene.List(Language, resolver=resolve_languages)

    word = graphene.Field(Morpheme, id=graphene.Int(), resolver=resolve_word)

    clauses = graphene.String(
        language_id=graphene.Int(),
        template=graphene.String(),
        tense=graphene.String(),
        number=graphene.String()
    )

    def resolve_clauses(self, info, language_id, template, tense, number):
        try:
            return json.dumps([create_clause(language_id, template, tense, number) for i in range(8)])
        except Exception as error:
            print "ERR:", error
            raise GraphQLError(error.message)

    derived_from = graphene.List(Derivation, id=graphene.Int())

    def resolve_derived_from(self, info, id):
        relationships = session.query(WordMorphemeModel).filter(
            WordMorphemeModel.word_id == id).all()
        derived_from = []

        for relationship in relationships:
            morpheme = session.query(MorphemeModel).get(
                relationship.morpheme_id)
            derivation = Derivation(
                relationship=relationship, morpheme=morpheme)
            derived_from.append(derivation)

        return derived_from


class Mutation(graphene.ObjectType):
    create_dictionary = CreateDictionary.Field()
    create_morpheme = CreateMorpheme.Field()
    create_language = CreateLanguage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

app = Flask(__name__)
app.debug = True

CORS(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )


)

if __name__ == '__main__':
    seed_db()
    app.run()
