import argparse
import sys

from sqlalchemy import inspect

from index import session, base, db

from tables.language import LanguageModel
from mocks.language import language_mocks

from tables.dictionary import DictionaryModel
from mocks.dictionary.index import dictionary_mocks

from tables.morpheme import MorphemeModel
from mocks.morpheme.index import morpheme_mocks


parser = argparse.ArgumentParser()
parser.add_argument('--lang', help='Language to seed the database')
args = parser.parse_args()


def table_names():
    names = inspect(db).get_table_names()
    return ", ".join(sorted(names))


def drop_db():
    print "dropping tables:", table_names()
    base.metadata.drop_all(db)
    session.commit()


def create_schema():
    base.metadata.create_all(db)
    session.commit()
    print "creating tables:", table_names()


def add(model):
    session.add(model)
    return session.commit()


def fill_tables(language):
    print "filling tables:", table_names()

    [add(LanguageModel(name=l.get("name"))) for l in language_mocks]

    [add(DictionaryModel(
        id=d.get("id"),
        data=d.get("data"),
        language_id=d.get("language_id")
    )) for d in dictionary_mocks[language]]

    [add(MorphemeModel(
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
    language = args.lang or "english"
    drop_db()
    create_schema()
    fill_tables(language)
