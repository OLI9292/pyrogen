import argparse
import sys

from sqlalchemy import inspect

from index import session, base, db

from tables.language import LanguageModel

from tables.dictionary import DictionaryModel
from mocks.dictionary.index import dictionary_mocks

from tables.morpheme import MorphemeModel
from mocks.morpheme.index import morpheme_mocks

from join_tables.word_morpheme import WordMorphemeModel
from mocks.word_morpheme import word_morpheme_mocks

parser = argparse.ArgumentParser()
parser.add_argument('--lang', help='Language to seed the database')
args = parser.parse_args()


def table_names():
    names = inspect(db).get_table_names()
    return ", ".join(sorted(names))


def drop_db():
    print("dropping tables:", table_names())
    base.metadata.drop_all(db)
    session.commit()


def create_schema():
    base.metadata.create_all(db)
    session.commit()
    print("creating tables:", table_names())


def add(model):
    session.add(model)
    return session.commit()


def fill_tables(language):
    print("filling " + language + " tables:", table_names())

    add(LanguageModel(name=language))

    [add(DictionaryModel(
        id=d.get("id"),
        data=d.get("data"),
        language_id=d.get("language_id")
    )) for d in dictionary_mocks[language]]

    [add(MorphemeModel(
        id=m.get("id"),
        value=m.get("value"),
        grammar=m.get("grammar"),
        copula=m.get("copula"),
        free=m.get("free"),
        animacy=m.get("animacy"),
        person=m.get("person"),
        irregular=m.get("irregular"),
        transitive=m.get("transitive"),
        intransitive=m.get("intransitive"),
        dictionary_id=m.get("dictionary_id"),
        language_id=m.get("language_id")
    )) for m in morpheme_mocks[language]]


def seed_db():
    LANGUAGES = ["english", "latin"]

    drop_db()
    create_schema()

    if args.lang != None:
        fill_tables(args.lang)
    else:
        for language in LANGUAGES:
            fill_tables(language)

        [add(WordMorphemeModel(
            word_id=w.get("word_id"),
            morpheme_id=w.get("morpheme_id"),
            value=w.get("value"),
            start_index=w.get("start_index")
        )) for w in word_morpheme_mocks]
