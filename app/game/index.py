from db.index import session

from db.tables.morpheme import Morpheme
from db.tables.word import Word
from db.tables.declension import Declension
from db.join_tables.word_morpheme import WordMorpheme


def list_questions():
    print "\n----------------\nlist questions\n----------------\n"
    for word in session.query(Word):
        print word.value
