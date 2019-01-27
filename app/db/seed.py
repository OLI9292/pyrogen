from sqlalchemy import inspect

from index import session, base, db

from tables.morpheme import Morpheme
from mocks.morpheme import morpheme_mocks

from tables.declension import Declension
from mocks.declension import declension_mocks

from tables.word import Word
from mocks.word import word_mocks

from join_tables.word_morpheme import WordMorpheme

#
# Helpers
#


def table_names():
    names = inspect(db).get_table_names()
    return ", ".join(sorted(names))


def add(obj, commit_and_return_id=False):
    session.add(obj)
    if commit_and_return_id:
        session.commit()
        session.refresh(obj)
        return obj.id


def create_word_and_morpheme_relationships(data):
    word = Word(value=data["value"], grammar=data["grammar"])
    word_id = add(word, True)
    for index, morpheme in enumerate(data["morphemes"]):
        morpheme_id = session.query(Morpheme).filter(
            Morpheme.value == morpheme).one().id
        word_morpheme = WordMorpheme(
            word_id=word_id, morpheme_id=morpheme_id, index=index)
        add(word_morpheme)


def describe_db():
    print "\ndeclensions"
    for declension in session.query(Declension):
        print "\t", declension.id, declension.data
    print "\nmorphemes"
    for morpheme in session.query(Morpheme):
        print "\t", morpheme.id, morpheme.value
    print "words"
    for word in session.query(Word):
        print "\t", word.id, word.value
    print "word-to-morpheme relationships"
    for word_morpheme in session.query(WordMorpheme):
        print "\t", word_morpheme.word_id, word_morpheme.morpheme_id, word_morpheme.index

#
# Seed db - drop db > create schema > fill tables
#


def drop_db():
    print "dropping tables:", table_names()
    base.metadata.drop_all(db)
    session.commit()


def create_schema():
    base.metadata.create_all(db)
    session.commit()
    print "creating tables:", table_names()


def fill_tables(language):
    print "filling tables"
    [add(Declension(name=d.get("name"), data=d.get("data")))
     for d in declension_mocks[language]]

    [add(Morpheme(value=m.get("value"), grammar=m.get("grammar"),
                  copula=m.get("copula"), free=m.get("free"), declension_id=m.get("declension_id"))) for m in morpheme_mocks[language]]

    [create_word_and_morpheme_relationships(w) for w in word_mocks[language]]


def seed_db(language, describe=False):
    print "\n----------------\nseeding database\n----------------\n"
    drop_db()
    create_schema()
    fill_tables(language)
    if describe:
        describe_db()
