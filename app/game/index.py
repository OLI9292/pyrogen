import random
from sqlalchemy.sql.expression import func, select

from db.index import session

from db.tables.dictionary import DictionaryModel
from db.tables.morpheme import MorphemeModel

from data.clause_types import clause_types

from lib.helpers import find_path_in_dict

tenses = ["present", "past"]
clauses = clause_types.keys()


def get_noun(lower_animacy=1, upper_animacy=10):
    results = session.query(MorphemeModel).filter(
        MorphemeModel.grammar == "noun",
        MorphemeModel.animacy <= upper_animacy,
        MorphemeModel.animacy >= lower_animacy,
    ).all()
    return random.choice(results)


def get_adjective():
    results = session.query(MorphemeModel).filter(
        MorphemeModel.grammar == "adjective").all()
    return random.choice(results)


def get_copula():
    return session.query(MorphemeModel).filter(MorphemeModel.copula == True).first()


def get_verb(use_transitive):
    filters = (
        MorphemeModel.grammar == "verb",
        MorphemeModel.intransitive == True
    ) if use_transitive else (
        MorphemeModel.grammar == "verb",
        MorphemeModel.intransitive == True
    )
    results = session.query(MorphemeModel).filter(*filters).all()
    return random.choice(results)


def decline_noun(value, dictionary, is_subject, is_object):
    if is_subject:
        value += dictionary["singular"]["nominative"]
    elif is_object:
        value += dictionary["singular"]["accusative"]

    article = session.query(DictionaryModel).filter(
        DictionaryModel.id == "article").first()

    if article:
        return article.data["definite"] + " " + value

    return value


def decline_verb(value, irregular, dictionary, tense, number, person):
    keys = [tense, number, person]
    if irregular:
        irregular_value = find_path_in_dict(keys, irregular)
        if irregular_value:
            return irregular_value
    ending = find_path_in_dict(keys, dictionary)
    if ending:
        value += ending
    return value


def decline_adjective(value, dictionary, is_subject):
    if is_subject:
        return value + dictionary["singular"]["nominative"]


def create_clause(template_key, tense_key):
    template_key = random.choice(
        clauses) if template_key == "random" else template_key
    clause = clause_types[template_key]

    print "generating elements for " + clause["full_name"]

    tense = random.choice(tenses) if tense_key == "random" else tense_key

    use_transitive = template_key == "SVO"
    person = ""
    number = "singular"

    sentence = []

    for element in clause["elements"]:
        if element == "subject":
            noun = get_noun(1, 2)
            person = str(noun.person)
            declined = decline_noun(
                noun.value, noun.dictionary.data, True, False)
            sentence.append(declined)

        elif element == "verb":
            verb = get_verb(use_transitive)
            declined = decline_verb(
                verb.value,
                verb.irregular,
                verb.dictionary.data,
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
                noun.value, noun.dictionary.data, False, True)
            sentence.append(declined)

        elif element == "predicate":
            adjective = get_adjective()

            # TODO: - adjective declensions
            #
            # declension = session.query(Declension).filter().all()
            # declined = decline_adjective(
            #     adjective.value, adjective.declension.data, True)

            sentence.append(adjective.value)

    return " ".join(sentence)
