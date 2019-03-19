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
from app.db.tables.morpheme import MorphemeModel, Morpheme, CreateMorpheme, resolve_morphemes, resolve_words, WordAndMorpheme, resolve_word
from app.db.tables.language import LanguageModel, Language, CreateLanguage, resolve_languages
from app.db.join_tables.word_morpheme import WordMorphemeModel, WordMorpheme
from app.game.index import create_clause
from app.scripts.import_wordcraft_words import migrate


class Query(graphene.ObjectType):
    dictionaries = graphene.List(Dictionary, resolver=resolve_dictionaries)

    morphemes = graphene.List(Morpheme, resolver=resolve_morphemes)

    languages = graphene.List(Language, resolver=resolve_languages)

    words = graphene.List(
        WordAndMorpheme,
        curriculum_id=graphene.String(),
        count=graphene.Int(required=False, default_value=None),
        resolver=resolve_words)

    word = graphene.Field(
        WordAndMorpheme, id=graphene.Int(), resolver=resolve_word)

    clauses = graphene.String(
        language_id=graphene.Int(),
        template=graphene.String(),
        tense=graphene.String(),
        number=graphene.String()
    )

    def resolve_clauses(self, info, language_id, template, tense, number):
        try:
            params = {
                "language_id": language_id,
                "template": template,
                "tense": tense,
                "number": number
            }
            return json.dumps([create_clause(params) for i in range(3)])
        except Exception as e:
            print("ERR:", e)


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
parser.add_argument('--migrate', help='Migrate OG Wordcraft')
args = parser.parse_args()


if __name__ == '__main__':
    if args.seed:
        seed_db(args.lang)
    if args.migrate:
        migrate()
    else:
        seed_db(None)
        # port = int(os.environ.get("PORT", 5000))
        # app.run(host='0.0.0.0', debug=False, port=port)
        # Hot Reload (Development)
        # app.run(host='0.0.0.0', debug=True, port=port)
