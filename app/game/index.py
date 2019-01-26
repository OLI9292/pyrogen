import random
from sqlalchemy.sql.expression import func, select

from db.index import session

from db.tables.morpheme import Morpheme
from db.tables.word import Word
from db.tables.declension import Declension
from db.join_tables.word_morpheme import WordMorpheme


def list_questions():
    print "\n----------------\ngenerate sentences\n----------------\n"
    words = session.query(Word)
    morphemes = session.query(Morpheme)
    for i in range(10):
        create_clause(words, morphemes)


clause_types = {
    "SVO": {
        "full_name": "subject verb object",
        "elements": ["subject", "verb", "object"]
    },
    "SV": {
        "full_name": "subject verb",
        "elements": ["subject", "verb"]
    },
    "S=P": {
        "full_name": "subject copula predicate",
        "elements": ["subject", "copula", "predicate"]
    },
    "S=": {
        "full_name": "existential use of the copula",
        "elements": ["subject", "copula"]
    }
}


def free_noun():
    results = session.query(Morpheme).filter(Morpheme.grammar == "noun").all()
    return random.choice(results)


def adjective():
    results = session.query(Morpheme).filter(
        Morpheme.grammar == "adjective").all()
    return random.choice(results)


def verb(copula=False):
    results = session.query(Morpheme).filter(
        Morpheme.grammar == "verb", Morpheme.copula == copula).all()
    return random.choice(results)


def create_clause(words, morphemes):
    key = random.choice(clause_types.keys())
    sentence = []

    for element in clause_types[key]["elements"]:
        if element == "subject":
            sentence.append(free_noun().value)
        elif element == "verb":
            sentence.append(verb().value)
        elif element == "copula":
            sentence.append(verb(True).value)
        elif element == "object":
            sentence.append(free_noun().value)
        else:
            sentence.append(adjective().value)

    print "\n", key
    print " ".join(sentence)
