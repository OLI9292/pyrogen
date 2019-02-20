from lib.helpers import flatten

from english.noun_endings import english_noun_endings
from english.verb_endings import english_verb_endings
from english.article import english_article

dictionary_mocks = {
    "english": flatten([
        english_noun_endings,
        english_verb_endings,
        english_article
    ])
}
