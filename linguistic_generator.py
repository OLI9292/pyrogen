from word_dictionaries import *
from latin_elements import *

def function_to_case(function):
    if function is "subject":
        return "nominative"
    else:
        return "accusative"
        
def make_noun(noun_object, function, number):
    function = function_to_case(function)
    family = noun_object["latin"]["family"]
    return {
        "type": "noun",
        "english" : {noun_object["english"][number]},
        "latin": {
            "beginning": noun_object["latin"]["stem"],
            "end": latin_noun_endings[family][number][function]
            } 
    }

def make_verb(verb_object, function, number, tense):
    function = function_to_case(function)
    family = verb_object["latin"]["family"]
    return {
        "type": "verb",
        "english" : {verb_object["english"][number][tense]},
        "latin": {
            "beginning": verb_object["latin"]["stem"],
            "middle": middle_elements_of_verbs[tense][family],
            "end": latin_verb_endings[number]
            } 
    }
