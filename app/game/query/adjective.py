import random

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel


def get_adjective(language_id):
    adjectives = session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "adjective",
        MorphemeModel.english_morpheme_id != None
    ).all()

    return random.choice(adjectives)


def decline_adjective(adjective, params):
    value = adjective.value

    if adjective.dictionary:
        dictionary = adjective.dictionary.data
        return value + dictionary[params["number"]][params["_type"]]

    return value
