import os
import sys
import random
from sqlalchemy.sql.expression import func, select

from app.db.index import session

from query.noun import get_noun_components
from query.adjective import get_adjective_component
from query.verb import get_verb_component, get_copula_component
from .data.clause_types import clause_types

from app.db.tables.language import LanguageModel

from app.lib.helpers import flatten

TENSES = ["present", "past", "future"]
NUMBERS = ["singular", "plural"]
CLAUSES = clause_types.keys()


def get_english_language_id():
    return session.query(LanguageModel).filter(
        LanguageModel.name == "english").first().id


def key_or_random(key, choices):
    return random.choice(choices) if key == "random" else key


def clause_params(params):
    tense = key_or_random(params["tense"], TENSES)
    number = key_or_random(params["number"], NUMBERS)
    template = key_or_random(params["template"], CLAUSES)
    clause = clause_types[template]

    return {
        "language_id": params["language_id"],
        "clause_name": clause["full_name"],
        "clause_elements": clause["elements"],
        "tense": tense,
        "number": number,
        "transitive": template == "SVO",
        "add_adjective": True,
        "upper_animacy": 10,
        "lower_animacy": 1,
        "translate": False,
        "adjectives": [],
        "nouns": [],
        "verbs": []
    }


def get_components(_type, params):
    if _type == "subject":
        return get_noun_components(dict(params, **{"_type": "nominative"}))
    elif _type == "verb":
        return get_verb_component(params)
    elif _type == "copula":
        return get_copula_component(params)
    elif _type == "object":
        return get_noun_components(dict(params, **{"_type": "accusative"}))
    elif _type == "predicate":
        return get_adjective_component(params)


def create_clause(params):
    params = params if "clause_name" in params else clause_params(params)
    print "\n",  "clause type: " + params["clause_name"]
    clause = []

    for _type in params["clause_elements"]:
        result = get_components(_type, params)
        params = result["params"]
        clause.append(result["components"])

    flattened = flatten(clause)
    print_clause(flattened)

    if not params["translate"]:
        params["language_id"] = get_english_language_id()
        params["translate"] = True
        create_clause(params)

    return flattened


def print_clause(clause):
    print " ".join([x["value"] for x in clause])

# {
#   TYPE: { type: String, required: true },
#   prompt: {
#     type: [
#       {
#         value: String,
#         isSentenceConnector: Boolean,
#         highlight: Boolean,
#         hide: Boolean
#       }
#     ]
#   },
#   answer: {
#     type: [
#       {
#         value: String,
#         prefill: Boolean,
#         isSentenceConnector: Boolean
#       }
#     ]
#   }
#   redHerrings: { type: [String], required: true },
#   curriculumId: { type: Schema.Types.ObjectId },
# }
