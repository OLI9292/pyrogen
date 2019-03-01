copula = {
    "value": "is",
    "irregular": {
        "present plural": "are",
        "present singular 1": "am",
        "past singular": "was",
        "past plural": "were",
        "future": "will be"
    },
    "grammar": "copula",
    "language_id": 1
}

article = {
    "value": "",
    "irregular": {
        "singular": ["a", "the"],
        "plural": "the",
    },
    "blacklist": ["personal"],
    "grammar": "article",
    "language_id": 1
}

english_special = [copula, article]
