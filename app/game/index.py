import random
from sqlalchemy.sql.expression import func, select

from db.index import session

from db.tables.dictionary import DictionaryModel
from db.tables.language import LanguageModel
from db.tables.morpheme import MorphemeModel

from data.clause_types import clause_types

from lib.helpers import find_path_in_dict, prepend_verb_ending

TENSES = ["present", "past", "future"]
NUMBERS = ["singular", "plural"]
CLAUSES = clause_types.keys()


def get_noun(language_id, lower_animacy=1, upper_animacy=10):
    results = session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "noun",
        MorphemeModel.animacy <= upper_animacy,
        MorphemeModel.animacy >= lower_animacy,
    ).all()
    return random.choice(results)


def get_adjective(language_id):
    results = session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "adjective"
    ).all()
    return random.choice(results)


def get_copula(language_id):
    return session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.copula == True
    ).first()


def get_verb(language_id, use_transitive):
    filters = (
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "verb",
        MorphemeModel.intransitive == True
    ) if use_transitive else (
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "verb",
        MorphemeModel.intransitive == True
    )
    results = session.query(MorphemeModel).filter(*filters).all()
    return random.choice(results)


def decline_noun(value, dictionary, number, is_subject, is_object, article):
    if is_subject:
        value += dictionary[number]["nominative"]
    elif is_object:
        value += dictionary[number]["accusative"]

    if article:
        return article.data["definite"] + " " + value

    return value


def decline_verb(value, irregular, dictionary, tense, number, person, language):
    # english past is appended
    # english future is prepended
    keys = [tense, number, person]

    if irregular:
        irregular_value = find_path_in_dict(keys, irregular)
        if irregular_value:
            return irregular_value

    ending = find_path_in_dict(keys, dictionary)

    if ending:
        if prepend_verb_ending(language, tense) == True:
            value = ending + " " + value
        else:
            value += ending

    return value


def decline_adjective(value, dictionary, is_subject):
    if is_subject:
        return value + dictionary["singular"]["nominative"]


def article_for_language(id):
    return session.query(DictionaryModel).filter(
        DictionaryModel.language_id == id,
        DictionaryModel.id == "article"
    ).first()


def create_clause(language_id, template_key, tense_key, number_key):
    language = session.query(LanguageModel).get(language_id).name
    template_key = random.choice(
        CLAUSES) if template_key == "random" else template_key
    clause = clause_types[template_key]

    print("generating elements for " + clause["full_name"])

    use_transitive = template_key == "SVO"
    article = article_for_language(language_id)
    tense = random.choice(TENSES) if tense_key == "random" else tense_key
    number = random.choice(NUMBERS) if number_key == "random" else number_key

    person = ""
    sentence = []

    for element in clause["elements"]:
        if element == "subject":
            noun = get_noun(language_id, 1, 2)

            person = str(noun.person)

            declined = decline_noun(
                noun.value,
                noun.dictionary.data,
                number,
                True,
                False,
                article
            )

            sentence.append({
                "id": noun.id,
                "value": declined,
                "in context": {
                    "use": "subject",
                    "person": noun.person
                }
            })

        elif element == "verb":
            verb = get_verb(language_id, use_transitive)

            declined = decline_verb(
                verb.value,
                verb.irregular,
                verb.dictionary.data,
                tense,
                number,
                person,
                language
            )

            sentence.append({
                "id": verb.id,
                "value": declined,
                "in context": {
                    "use": "verb",
                    "tense": tense,
                    "number": number,
                    "person": person
                }
            })

        elif element == "copula":
            copula = get_copula(language_id)

            declined = decline_verb(
                copula.value,
                copula.irregular,
                {},
                tense,
                number,
                person,
                language
            )

            sentence.append({
                "id": copula.id,
                "value": declined,
                "in context": {
                    "use": "copula"
                }
            })

        elif element == "object":
            noun = get_noun(language_id)

            declined = decline_noun(
                noun.value,
                noun.dictionary.data,
                number,
                False,
                True,
                article
            )

            sentence.append({
                "id": noun.id,
                "value": declined,
                "in context": {
                    "use": "object"
                }
            })

        elif element == "predicate":
            adjective = get_adjective(language_id)

            # TODO: - adjective declensions
            #
            # declension = session.query(Declension).filter().all()
            # declined = decline_adjective(
            #     adjective.value, adjective.declension.data, True)

            sentence.append({
                "id": adjective.id,
                "value": adjective.value,
                "in context": {
                    "use": "predicate"
                }
            })

    return sentence
