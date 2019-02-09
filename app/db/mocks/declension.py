english_declension_mocks = [
    {
        "id": "first",
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
    },
    {
        "id": "I",
        "data": {
            "singular": {
                "nominative": "I",
                "accusative": "me",
            },
            "plural": {
                "nominative": "we",
                "accusative": "us",
            }
        }
    }
]

latin_declension_mocks = [
    {
        "id": "first",
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
        "id": "second",
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
    "english": english_declension_mocks,
    "latin": latin_declension_mocks
}
