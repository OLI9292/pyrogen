from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

import graphene
from flask_graphql import GraphQLView
from graphql import GraphQLError

from db.seed import seed_db
from db.tables.dictionary import DictionaryModel, Dictionary, CreateDictionary, resolve_dictionaries
from db.tables.morpheme import MorphemeModel, Morpheme, CreateMorpheme, resolve_morphemes
from db.tables.language import LanguageModel, Language, CreateLanguage, resolve_languages
from game.index import create_clause


class Query(graphene.ObjectType):
    dictionaries = graphene.List(Dictionary, resolver=resolve_dictionaries)
    morphemes = graphene.List(Morpheme, resolver=resolve_morphemes)
    languages = graphene.List(Language, resolver=resolve_languages)
    clauses = graphene.List(
        graphene.String, template=graphene.String(), tense=graphene.String())

    def resolve_clauses(self, info, template, tense):
        try:
            return [create_clause(template, tense) for i in range(10)]
        except Exception as error:
            print "ERR:", error
            raise GraphQLError(error.message)


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
