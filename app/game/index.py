import os
import sys
import random
from sqlalchemy.sql.expression import func, select

from app.db.index import session

from query.noun import get_noun, decline_noun
from query.adjective import get_adjective, decline_adjective
from query.verb import get_verb, get_copula, decline_verb
from .data.clause_types import clause_types

from app.db.tables.language import LanguageModel

from app.lib.helpers import flatten

TENSES = ["present", "past", "future"]
NUMBERS = ["singular", "plural"]
CLAUSES = clause_types.keys()

# PARAMS FOR CLAUSE
#
# Clause Type
# Tense
# Number
#
# Random Noun, Verb, Adjective, Article


def create_clause(language_id, template_key, tense_key, number_key):
    try:
        language = session.query(LanguageModel).get(language_id).name
        template_key = random.choice(
            CLAUSES) if template_key == "random" else template_key
        clause_data = clause_types[template_key]

        print("generating elements for " + clause_data["full_name"])

        use_transitive = template_key == "SVO"
        tense = random.choice(TENSES) if tense_key == "random" else tense_key
        number = random.choice(
            NUMBERS) if number_key == "random" else number_key

        person = ""
        clause = []

        for element in clause_data["elements"]:
            if element == "subject":
                params = {"number": number, "_type": "nominative"}
                add_adjective = True
                data = get_noun(language_id, add_adjective, params)
                person = data["person"]
                clause.append(data["components"])

            elif element == "verb":
                params = {"number": number, "tense": tense, "person": person}
                verb_components = get_verb(language_id, use_transitive, params)
                clause.append(verb_components)

            elif element == "copula":
                params = {"number": number, "tense": tense, "person": person}
                copula_components = get_copula(language_id, params)
                clause.append(copula_components)

            elif element == "object":
                params = {"number": number, "_type": "accusative"}
                data = get_noun(language_id, True, params)
                clause.append(data["components"])

            elif element == "predicate":
                adjective = get_adjective(language_id)

                clause.append([{
                    "id": adjective.id,
                    "value": adjective.value,
                    "in context": {
                        "use": "predicate"
                    }
                }])

        flattened = flatten(clause)
        return flattened

    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERR: create_clause", exc_type, fname, exc_tb.tb_lineno)
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
