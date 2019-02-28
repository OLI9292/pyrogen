import random

from app.db.index import session
from app.db.tables.morpheme import MorphemeModel
from adjective import get_adjective, decline_adjective
from other import article_for_language

case_to_type_mapping = {
    "nominative": "subject",
    "accusative": "object",
}


def get_noun(language_id, add_adjective, params, lower_animacy=1, upper_animacy=10):
    components = []
    noun_type = case_to_type_mapping[params["_type"]]
    article = article_for_language(language_id)

    nouns = session.query(MorphemeModel).filter(
        MorphemeModel.language_id == language_id,
        MorphemeModel.grammar == "noun",
        MorphemeModel.animacy <= upper_animacy,
        MorphemeModel.animacy >= lower_animacy,
    ).all()
    noun = random.choice(nouns)
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

    if add_adjective:
        adjective = get_adjective(language_id)
        declined_adjective = decline_adjective(adjective, params)
        adjective_component = {
            "id": adjective.id,
            "value": declined_adjective,
            "in context": {
                "use": "adjective modifying " + noun_type,
            }
        }
        components.insert(0, adjective_component)

    if article:
        article_component = {
            "id": article.id,
            "value": article.data["definite"],
            "in context": {
                "use": "article",
            }
        }
        components.insert(0, article_component)

    return {"components": components, "person": str(noun.person)}


def decline_noun(noun, params):
    dictionary = noun.dictionary.data
    return noun.value + dictionary[params["number"]][params["_type"]]
