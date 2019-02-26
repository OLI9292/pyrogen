from app.lib.helpers import flatten

from english.noun_endings import english_noun_endings
from english.verb_endings import english_verb_endings
from english.article import english_article

from latin.noun_endings import latin_noun_endings
from latin.verb_endings import latin_verb_endings

dictionary_mocks = {
    "english": flatten([
        english_noun_endings,
        english_verb_endings,
        english_article
    ]),
    "latin": flatten([
        latin_noun_endings,
        latin_verb_endings,
    ])
}
