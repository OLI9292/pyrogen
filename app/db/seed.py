from sqlalchemy import inspect

from index import session, base, db

from tables.language import LanguageModel

from tables.dictionary import DictionaryModel
from mocks.dictionary.index import dictionary_mocks

from tables.morpheme import MorphemeModel
from mocks.morpheme.index import morpheme_mocks

from join_tables.word_morpheme import WordMorphemeModel
from mocks.word_morpheme import word_morpheme_mocks

LANGUAGES = ["english", "latin"]


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


def setup_db():
    drop_db()
    create_schema()
    for language in LANGUAGES:
        add(LanguageModel(name=language))


def fill_tables(language):
    print("filling " + language + " tables:", table_names())

    [add(DictionaryModel(
        id=d.get("id"),
        data=d.get("data"),
        language_id=d.get("language_id")
    )) for d in dictionary_mocks[language]]

    [add(MorphemeModel(
        id=m.get("id"),
        value=m.get("value"),
        grammar=m.get("grammar"),
        free=m.get("free"),
        definition=m.get("definition"),
        animacy=m.get("animacy"),
        noun_attributes=m.get("noun_attributes"),
        blacklist=m.get("blacklist"),
        person=m.get("person"),
        irregular=m.get("irregular"),
        transitive=m.get("transitive"),
        intransitive=m.get("intransitive"),
        dictionary_id=m.get("dictionary_id"),
        curriculum_id=m.get("curriculum_id"),
        language_id=m.get("language_id"),
        english_morpheme_id=m.get("english_morpheme_id"),
        template_id=m.get("template_id"),
        properties=m.get("properties"),
    )) for m in morpheme_mocks[language]]


def seed_db(lang):
    setup_db()
    if lang != None:
        fill_tables(lang)
    else:
        for language in LANGUAGES:
            fill_tables(language)

        [add(WordMorphemeModel(
            word_id=w.get("word_id"),
            morpheme_id=w.get("morpheme_id"),
            value=w.get("value"),
            start_index=w.get("start_index"),
            definition_start_index=w.get("definition_start_index"),
            definition_end_index=w.get("definition_end_index"),
        )) for w in word_morpheme_mocks]
