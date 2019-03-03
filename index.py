import argparse
import sys
import json
import os
from flask import Flask

from flask_cors import CORS

import graphene
from flask_graphql import GraphQLView

from app.db.seed import seed_db, session
from app.db.tables.dictionary import DictionaryModel, Dictionary, CreateDictionary, resolve_dictionaries
from app.db.tables.morpheme import MorphemeModel, Morpheme, CreateMorpheme, resolve_morphemes, resolve_word
from app.db.tables.language import LanguageModel, Language, CreateLanguage, resolve_languages
from app.db.join_tables.word_morpheme import WordMorphemeModel, WordMorpheme
from app.game.index import create_clause


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
            return json.dumps([create_clause(language_id, template, tense, number) for i in range(3)])
        except Exception as e:
            print("ERR:", e)

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

parser = argparse.ArgumentParser()
parser.add_argument('--lang', help='Language to seed the database')
parser.add_argument('--seed', help='Seed database')
args = parser.parse_args()


if __name__ == '__main__':
    if args.seed:
        seed_db(args.lang)
    else:
        seed_db(None)
        port = int(os.environ.get("PORT", 5000))
        # app.run(host='0.0.0.0', debug=False, port=port)
        # Hot Reload (Development)
        app.run(host='0.0.0.0', debug=True, port=port)
