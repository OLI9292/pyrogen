import random

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel

from app.lib.helpers import find_path_in_dict, prepend_verb_ending


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


def decline_verb(value, irregular, dictionary, tense, number, person, language):
    # english past is appended
    # english future is prepended
    keys = [tense, number, person]
    print keys

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
