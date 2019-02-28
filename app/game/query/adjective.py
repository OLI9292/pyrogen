import random

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel


def get_adjective(language_id):
    results = session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "adjective"
    ).all()
    return random.choice(results)


def decline_adjective(adjective, params):
    value = adjective.value
    if adjective.dictionary:
        dictionary = adjective.dictionary.data
        return value + dictionary[params["number"]][params["_type"]]
    return value
