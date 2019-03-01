import random

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel
from app.db.tables.language import LanguageModel

from app.lib.helpers import find_path_in_dict


def prepend_verb_ending(language, tense):
    if (language.name == "english") & (tense == "future"):
        return True
    return False


def get_copula(language_id, params):
    copula = session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "copula"
    ).first()

    declined_copula = decline_verb(language_id, copula, params)

    return [{
        "id": copula.id,
        "value": declined_copula,
        "in context": {
            "use": "copula",
        }
    }]

# def translate_to_english(verb, params):


def get_verb(language_id, use_transitive, params):
    filters = (
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "verb",
        MorphemeModel.transitive == True,
        MorphemeModel.english_morpheme_id != None
    ) if use_transitive else (
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "verb",
        MorphemeModel.intransitive == True,
        MorphemeModel.english_morpheme_id != None
    )

    verbs = session.query(MorphemeModel).filter(*filters).all()
    verb = random.choice(verbs)
    declined_verb = decline_verb(language_id, verb, params)

    return [{
        "id": verb.id,
        "value": declined_verb,
        "in context": {
            "use": "article",
        }
    }]


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
