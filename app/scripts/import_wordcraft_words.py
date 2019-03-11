import requests

from ..db.index import session, base, db
from ..db.seed import setup_db

from ..db.tables.language import LanguageModel
from ..db.tables.morpheme import MorphemeModel
from ..db.join_tables.word_morpheme import WordMorphemeModel


ROOTS_URL = "https://desolate-plains-35942.herokuapp.com/api/v2/roots"
WORDS_URL = "https://desolate-plains-35942.herokuapp.com/api/v2/words"


def get_or_create(model, kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return False, instance
    else:
        params = dict((k, v) for k, v in kwargs.iteritems())
        instance = model(**params)
        session.add(instance)
        session.flush()
        session.refresh(instance)
        return True, instance


def value_index(components, root):
    index = 0
    for c in components:
        if c["value"] == root:
            return index
        else:
            index += len(c["value"])


def definition_indexes(components, root_definitions):
    index = 0
    for c in components:
        if c["isRoot"] & (c["value"] in root_definitions):
            return [index, index + len(c["value"]) - 1]
        else:
            index += len(c["value"])


def create_word_and_roots(word_data, roots_data):
    word_params = {
        "value": word_data["value"],
        "curriculum_id": "5c110cfc6aa666a547278e98",
        "definition": "".join([d["value"] for d in word_data["definition"]])
    }

    [is_new, word] = get_or_create(MorphemeModel, word_params)
    print "created", word.value, word.id

    for data in roots_data:
        root_params = {
            "value": data["value"],
            "language_id": 2
        }

        [is_new, root] = get_or_create(MorphemeModel, root_params)

        start_index = value_index(word_data["components"], root.value)
        [definition_start_index, definition_end_index] = definition_indexes(
            word_data["definition"], data["definitions"])

        relationship_params = {
            "word_id": word.id,
            "morpheme_id": root.id,
            "value": root.value,
            "definition_start_index": definition_start_index,
            "definition_end_index": definition_end_index,
            "start_index": start_index,
        }

        get_or_create(WordMorphemeModel, relationship_params)


def migrate():
    setup_db()

    roots = requests.get(ROOTS_URL).json()
    words = requests.get(WORDS_URL).json()

    for word in words:
        word_roots = [root for root in roots if root["_id"] in word["roots"]]
        create_word_and_roots(word, word_roots)

    session.commit()
