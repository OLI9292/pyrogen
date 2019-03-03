import random
import sys

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel


def random_adjective(params):
    filters = [
        MorphemeModel.language_id == params["language_id"],
        MorphemeModel.grammar == "adjective"
    ]
    if not params["translate"]:
        filters.append(MorphemeModel.english_morpheme_id != None)
    return random.choice(session.query(MorphemeModel).filter(*filters).all())


def get_adjective_component(params):
    try:
        adjective = session.query(MorphemeModel).get(
            params["adjectives"].pop(0)) if params["translate"] else random_adjective(params)
        declined = decline_adjective(adjective, params)

        if not params["translate"]:
            params["adjectives"].append(
                adjective.english_morpheme_id)

        component = {
            "id": adjective.id,
            "value": declined,
            "in context": {
                "use": "adjective",
            }
        }

        return {"params": params, "components": [component]}
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ERR: get_noun_components", error, exc_tb.tb_lineno)
        return []


def decline_adjective(adjective, params):
    value = adjective.value

    if adjective.dictionary:
        dictionary = adjective.dictionary.data
        return value + dictionary[params["number"]][params["_type"]]

    return value
