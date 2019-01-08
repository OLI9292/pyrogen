from word_dictionaries import *

nouns_dict = nouns_dictionary
verbs_dict = verbs_dictionary
# question sequence
levels = [{
    "number": ["singular"], 
    "tense": ["present"],
    "nouns" : ["bear", "horse"],
    "verbs" : ["love"],
    }, {
    "number": ["singular"], 
    "tense": ["present", "past", "future"],
    "nouns" : ["wolf", "bear", "horse"],
    "verbs" : ["eat", "carry"],
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present"],
    "nouns" : ["bear", "horse"],
    "verbs" : ["love"],
    },
     {
    "number": ["singular", "plural"], 
    "tense": ["present", "past", "future"],
    "nouns" : ["bear", "horse"],
    "verbs" : ["love"],
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present", "past", "future"],
    "nouns" : ["wolf", "bear", "horse", "frog"],
    "verbs" : ["love", "carry", "attack"],
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present"],
    "nouns" : ["wolf", "bear", "horse", "frog"],
    "verbs" : ["carry", "fear", "scare", "see"],
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present", "past", "future"],
    "nouns" : ["wolf", "bear", "horse", "frog"],
    "verbs" : ["love", "eat", "scare", "see"],
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present", "past", "future"],
    "nouns" : ["kangaroo"],
    "verbs" : ["carry"],
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present", "past", "future"],
    "nouns" : ["crow", "wolf", "bear", "horse", "fly", "eagle", "octopus"],
    "verbs" : ["carry"],
    },
    {
    "number": ["singular"], 
    "tense": ["present", "past", "future"],
    "nouns" : ["crow", "spider", "chicken", "horse", "fly", "eagle", "octopus"],
    "verbs" : ["carry"],
    },
    {
    "number": ["singular"], 
    "tense": ["present", "future"],
    "nouns" : ["crocodile", "frog", "lizard", "kangaroo"],
    "verbs" : ["carry"],
    },
    {
    "number": ["singular", "plural"], 
    "tense":  ["present", "future"],
    "nouns" : ["wolf", "bear", "horse", "frog"],
    "verbs" : ["carry", "fear", "scare", "see"],
    },
    {
    "number": ["singular"], 
    "tense": ["present"],
    "nouns" : list(nouns_dict.keys()),
    "verbs" : list(verbs_dict.keys()),
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present"],
    "nouns" : list(nouns_dict.keys()),
    "verbs" : list(verbs_dict.keys()),
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present", "future"],
    "nouns" : list(nouns_dict.keys()),
    "verbs" : list(verbs_dict.keys()),
    },
    {
    "number": ["singular", "plural"], 
    "tense": ["present", "past", "future"],
    "nouns" : list(nouns_dict.keys()),
    "verbs" : list(verbs_dict.keys()),
    }
]
