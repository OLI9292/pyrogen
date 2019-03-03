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


def get_english_lanugage_id():
    return session.query(LanguageModel).filter(
        LanguageModel.name == "english").first().id


def key_or_random(key, choices):
    return random.choice(choices) if key == "random" else key


def clause_params(language_id, template, tense, number):
    tense = key_or_random(tense, TENSES)
    number = key_or_random(number, NUMBERS)
    template = key_or_random(template, CLAUSES)
    clause = clause_types[template]

    return {
        "language_id": language_id,
        "english_id": get_english_lanugage_id(),
        "clause_name": clause["full_name"],
        "clause_elements": clause["elements"],
        "tense": tense,
        "number": number,
        "transitive": template == "SVO",
        "add_adjective": True,
        "upper_animacy": 10,
        "lower_animacy": 1
    }


def create_clause(language_id, template, tense, number):
    try:
        params = clause_params(language_id, template, tense, number)
        print "\n\n", "clause type: " + params["clause_name"], "\n"

        clause = []
        # english_clause = []

        for element in params["clause_elements"]:
            if element == "subject":
                data = get_noun_components(
                    dict(params, **{"_type": "nominative"}))
                params = data["params"]
                clause.append(data["components"])
                # english_clause.append(get_noun_components(
                #     english_id, params, data["english_noun_id"], data["english_adjective_id"])["components"])

            elif element == "verb":
                verb_component = get_verb_component(params)
                clause.append([verb_component])
                # english_clause.append([get_verb_component(
                #     english_id, params, verb_component["english_id"])])

            elif element == "copula":
                copula_components = get_copula_component(params)
                clause.append([copula_components])
                # english_clause.append(
                #     get_copula_component(english_id, params))

            elif element == "object":
                data = get_noun_components(
                    dict(params, **{"_type": "accusative"}))
                clause.append(data["components"])

                # english_clause.append(get_noun_components(
                #     english_id, params, data["english_noun_id"], data["english_adjective_id"])["components"])

            elif element == "predicate":
                adjective_component = get_adjective_component(params)
                clause.append([adjective_component])

                # english_clause.append([get_adjective_component(
                #     english_id, params, adjective_component["english_id"])])

        flattened = flatten(clause)
        # english_flattened = flatten(english_clause)
        # print "\n", " ".join([x["value"] for x in flattened]
        #                      ), " - ", " ".join([x["value"] for x in english_flattened]), "\n\n"
        return flattened

    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERR: create_clause", error, exc_type, fname, exc_tb.tb_lineno)
        return []


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
