from lib.helpers import flatten

from english.verb import english_verbs
from english.noun import english_nouns
from english.adjective import english_adjectives

from latin.verb import latin_verbs
from latin.noun import latin_nouns
from latin.adjective import latin_adjectives

morpheme_mocks = {
    "english": flatten([
        english_nouns,
        english_verbs,
        english_adjectives
    ]),
    "latin": flatten([
        latin_nouns,
        latin_verbs,
        latin_adjectives
    ])
}
