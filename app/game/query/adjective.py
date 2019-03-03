import random

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel


def random_adjective(language_id):
    return random.choice(session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "adjective",
        # MorphemeModel.english_morpheme_id != None
    ).all())


def get_adjective_component(params, adjective_id=None):
    adjective = session.query(MorphemeModel).get(
        adjective_id) if adjective_id else random_adjective(params["language_id"])
    declined = decline_adjective(adjective, params)

    return {
        "id": adjective.id,
        "english_id": adjective.english_morpheme_id,
        "value": declined,
        "in context": {
            "use": "adjective",
        }
    }


def decline_adjective(adjective, params):
    value = adjective.value

    if adjective.dictionary:
        dictionary = adjective.dictionary.data
        return value + dictionary[params["number"]][params["_type"]]

    return value
