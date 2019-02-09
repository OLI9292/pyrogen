import random
from sqlalchemy.sql.expression import func, select

from db.index import session

from db.tables.article import Article
from db.tables.morpheme import Morpheme
from db.tables.word import Word
from db.tables.declension import Declension

from db.join_tables.word_morpheme import WordMorpheme

from lib.helpers import find_path_in_dict


def list_questions():
    print "\n----------------\ngenerate sentences\n----------------\n"
    words = session.query(Word)
    morphemes = session.query(Morpheme)
    for i in range(20):
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


def get_noun(lower_animacy=1, upper_animacy=10):
    results = session.query(Morpheme).filter(
        Morpheme.grammar == "noun",
        Morpheme.animacy <= upper_animacy,
        Morpheme.animacy >= lower_animacy,
    ).all()
    return random.choice(results)


def get_adjective():
    results = session.query(Morpheme).filter(
        Morpheme.grammar == "adjective").all()
    return random.choice(results)


def get_copula():
    return session.query(Morpheme).filter(Morpheme.copula == True).first()


def get_verb(use_transitive):
    filters = (
        Morpheme.grammar == "verb",
        Morpheme.intransitive == True
    ) if use_transitive else (
        Morpheme.grammar == "verb",
        Morpheme.intransitive == True
    )
    results = session.query(Morpheme).filter(*filters).all()
    return random.choice(results)


def decline_noun(value, declension, is_subject, is_object):
    if is_subject:
        value += declension["singular"]["nominative"]
    elif is_object:
        value += declension["singular"]["accusative"]

    article = session.query(Article).first()

    if article:
        return article.data["definite"] + " " + value

    return value


def decline_verb(value, irregular, conjugation, tense, number, person):
    keys = [tense, number, person]
    if irregular:
        irregular_value = find_path_in_dict(keys, irregular)
        if irregular_value:
            return irregular_value
    ending = find_path_in_dict(keys, conjugation)
    if ending:
        value += ending
    return value


def decline_adjective(value, declension, is_subject):
    if is_subject:
        return value + declension["singular"]["nominative"]


def create_clause(words, morphemes):
    # key = "SVO"
    key = random.choice(clause_types.keys())

    clause = clause_types[key]["elements"]
    use_transitive = key == "SVO"

    tense = random.choice(["present", "past"])
    person = ""
    number = "singular"

    sentence = []

    for element in clause:
        if element == "subject":
            noun = get_noun(1, 2)
            person = str(noun.person)
            declined = decline_noun(
                noun.value, noun.declension.data, True, False)
            sentence.append(declined)

        elif element == "verb":
            verb = get_verb(use_transitive)
            declined = decline_verb(
                verb.value,
                verb.irregular,
                verb.conjugation.data,
                tense,
                number,
                person
            )
            sentence.append(declined)

        elif element == "copula":
            sentence.append(get_copula().value)

        elif element == "object":
            noun = get_noun()
            declined = decline_noun(
                noun.value, noun.declension.data, False, True)
            sentence.append(declined)

        elif element == "predicate":
            adjective = get_adjective()

            # TODO: - adjective declensions
            #
            # declension = session.query(Declension).filter().all()
            # declined = decline_adjective(
            #     adjective.value, adjective.declension.data, True)

            sentence.append(adjective.value)

    # print "\n", key
    print " ".join(sentence)
