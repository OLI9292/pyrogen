import random
import sys

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel
from app.db.tables.language import LanguageModel

from app.lib.helpers import find_path_in_dict


def prepend_verb_ending(language, tense):
    if (language.name == "english") & (tense == "future"):
        return True
    return False


def get_copula_component(params):
    filters = [
        MorphemeModel.language_id == params["language_id"],
        MorphemeModel.grammar == "copula"
    ]
    copula = session.query(MorphemeModel).filter(*filters).first()
    declined_copula = decline_verb(params["language_id"], copula, params)
    component = {
        "id": copula.id,
        "value": declined_copula,
        "in context": {
            "use": "copula",
        }
    }
    return {"params": params, "components": [component]}


def get_random_verb(params):
    filters = [
        MorphemeModel.language_id == params["language_id"],
        MorphemeModel.grammar == "verb",
    ]
    if params["transitive"]:
        filters.append(MorphemeModel.transitive)
    else:
        filters.append(MorphemeModel.intransitive)
    if not params["translate"]:
        filters.append(MorphemeModel.english_morpheme_id != None)
    verbs = session.query(MorphemeModel).filter(*filters).all()
    return random.choice(verbs)


def get_verb_component(params):
    try:
        verb = session.query(MorphemeModel).get(
            params["verbs"].pop(0)) if params["translate"] else get_random_verb(params)
        declined_verb = decline_verb(params["language_id"], verb, params)

        component = {
            "id": verb.id,
            "value": declined_verb,
            "in context": {
                "use": "verb",
            }
        }

        if not params["translate"]:
            params["verbs"].append(verb.english_morpheme_id)

        return {"params": params, "components": [component]}
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ERR: get_verb_component", error, exc_tb.tb_lineno)
        return []


def decline_verb(language_id, verb, params):
    language = session.query(LanguageModel).get(language_id)
    value = verb.value

    keys = [params["tense"], params["number"], params["person"]]

    if verb.irregular:
        irregular_value = find_path_in_dict(keys, verb.irregular)
        if irregular_value:
            return irregular_value

    if verb.dictionary:
        ending = find_path_in_dict(keys, verb.dictionary.data)
        if ending:
            if prepend_verb_ending(language, params["tense"]):
                value = ending + " " + value
            else:
                value += ending

    return value
