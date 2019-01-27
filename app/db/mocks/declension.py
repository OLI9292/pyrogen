english_conjugation_mocks = [
    {
        "name": "first",
        "data": {
            "singular": {
                "nominative": "",
                "accusative": "",
            },
            "plural": {
                "nominative": "s",
                "accusative": "s",
            }
        }
    }
]

latin_declension_mocks = [
    {
        "name": "first",
        "data": {
            "singular": {
                "nominative": "a",
                "accusative": "am",
            },
            "plural": {
                "nominative": "ae",
                "accusative": "as",
            }
        }
    },
    {
        "name": "second",
        "data":  {
            "singular": {
                "nominative": "us",
                "accusative": "um",
            },
            "plural": {
                "nominative": "i",
                "accusative": "os",
            }
        }
    }
]

declension_mocks = {
    "english": english_conjugation_mocks,
    "latin": latin_declension_mocks
}
