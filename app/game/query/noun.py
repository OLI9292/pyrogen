import random
import os
import sys

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel
from adjective import get_adjective_component, decline_adjective
from other import get_article_components, get_article

from app.lib.helpers import find_path_in_dict

CASE_TO_TYPE_MAPPING = {
    "nominative": "subject",
    "accusative": "object",
}


def can_add_article(noun, article):
    blacklist = set(article.blacklist)
    noun_attributes = set(noun.noun_attributes or [])
    return len(list(blacklist.intersection(noun_attributes))) == 0


def can_add_adjective(noun):
    attributes = noun.noun_attributes or []
    return not "personal" in attributes


def random_noun(params):
    filters = [
        MorphemeModel.language_id == params["language_id"],
        MorphemeModel.grammar == "noun",
        MorphemeModel.animacy <= params["upper_animacy"],
        MorphemeModel.animacy >= params["lower_animacy"],
    ]
    if params["translate"]:
        filters.append(MorphemeModel.english_morpheme_id != None)
    return random.choice(session.query(MorphemeModel).filter(*filters).all())


def get_noun_components(params):
    try:
        result = {}
        components = []
        noun_type = CASE_TO_TYPE_MAPPING[params["_type"]]

        noun = session.query(MorphemeModel).get(
            params["nouns"].pop(0)) if params["nouns"] else random_noun(params)

        params["person"] = str(noun.person)

        if params["translate"]:
            params["nouns"].append(noun.english_morpheme_id)

        declined_noun = decline_noun(noun, params)
        noun_component = {
            "id": noun.id,
            "value": declined_noun,
            "in context": {
                "use": noun_type,
                "person": noun.person
            }
        }
        components.append(noun_component)

        if params["add_adjective"] and can_add_adjective(noun):
            result = get_adjective_component(params)
            component = result["components"][0]
            params = result["params"]
            components.insert(0, component)

        article = get_article(params)
        if article and can_add_article(noun, article):
            result = get_article_components(article, params)
            component = result["components"][0]
            params = result["params"]
            components.insert(0, component)

        result["components"] = components
        result["params"] = params
        return result

    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ERR: get_noun_components", error, exc_tb.tb_lineno)
        return []


def decline_noun(noun, params):
    dictionary = noun.dictionary.data

    if noun.irregular:
        keys = [params["number"]]
        irregular_value = find_path_in_dict(keys, noun.irregular)
        if irregular_value:
            return irregular_value

    return noun.value + dictionary[params["number"]][params["_type"]]
