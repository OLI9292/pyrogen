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
    copula = session.query(MorphemeModel).filter(
        MorphemeModel.language_id == params["language_id"],
        MorphemeModel.grammar == "copula"
    ).first()

    declined_copula = decline_verb(params["language_id"], copula, params)

    return {
        "id": copula.id,
        "value": declined_copula,
        "in context": {
            "use": "copula",
        }
    }


def get_random_verb(language_id, transitive):
    filters = (
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "verb",
        MorphemeModel.transitive,
        # MorphemeModel.english_morpheme_id != None
    ) if transitive else (
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "verb",
        MorphemeModel.intransitive,
        # MorphemeModel.english_morpheme_id != None
    )

    verbs = session.query(MorphemeModel).filter(*filters).all()
    return random.choice(verbs)


def get_verb_component(params, verb_id=None):
    try:
        verb = session.query(MorphemeModel).get(
            verb_id) if verb_id else get_random_verb(params["language_id"], params["transitive"])
        declined_verb = decline_verb(params["language_id"], verb, params)
        return {
            "id": verb.id,
            "english_id": verb.english_morpheme_id,
            "value": declined_verb,
            "in context": {
                "use": "verb",
            }
        }
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
