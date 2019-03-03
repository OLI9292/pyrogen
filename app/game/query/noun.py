import random
import os
import sys

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel
from adjective import get_adjective_component, decline_adjective
from other import article_for_language, decline_article

from app.lib.helpers import find_path_in_dict

case_to_type_mapping = {
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


def random_noun(language_id, params):
    return random.choice(session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "noun",
        MorphemeModel.animacy <= params["upper_animacy"],
        MorphemeModel.animacy >= params["lower_animacy"],
        # MorphemeModel.english_morpheme_id != None
    ).all())


def get_noun_components(params, noun_id=None, adjective_id=None):
    try:
        result = {}
        components = []
        noun_type = case_to_type_mapping[params["_type"]]
        article = article_for_language(params["language_id"])

        noun = session.query(MorphemeModel).get(
            noun_id) if noun_id else random_noun(params["language_id"], params)
        params["person"] = str(noun.person)
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
            adjective_component = get_adjective_component(params, adjective_id)
            result["english_adjective_id"] = adjective_component["english_id"]
            components.insert(0, adjective_component)

        if article and can_add_article(noun, article):
            declined_article = decline_article(article, params)
            article_component = {
                "id": article.id,
                "value": declined_article,
                "in context": {
                    "use": "article",
                }
            }
            components.insert(0, article_component)

        result["components"] = components
        result["params"] = params
        result["english_noun_id"] = noun.english_morpheme_id
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
