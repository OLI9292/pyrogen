import random

from word_dictionaries import *
from latin_elements import *

from sequence import *

def decline_noun(noun_object, case, number):
    gender = noun_object["latin"]["gender"]
    ending = latin_noun_endings[gender][case][number]
    return noun_object["latin"]["stem"] + ending

def make_verb(verb_object, verb_number, tense):
    return verb_object[verb_number][tense]

def make_latin_sentence(sentence_object):
    latin_subject = decline_noun(sentence_object["subject"], "subject", sentence_object["subject_number"])

    latin_object = decline_noun(sentence_object["object"], "object", sentence_object["object_number"])

    verb_number = sentence_object["subject_number"]
    latin_verb = make_verb(sentence_object["verb"]["latin"], verb_number, sentence_object["tense"])
    shuffled = [latin_subject, latin_verb, latin_object]
    random.shuffle(shuffled)
    return " ".join(shuffled)

def make_english_sentence(sentence_object):
    english_subject = sentence_object["subject"]["english"][sentence_object["subject_number"]]
    english_object = sentence_object["object"]["english"][sentence_object["object_number"]] 
    english_verb = sentence_object["verb"]["english"][sentence_object["subject_number"]][sentence_object["tense"]]
    return "the " + english_subject + " " + english_verb + " " + "the " + english_object

def make_choices(sentence_object, params):
    make_choices = []
    for tense in params["tense"]:
        for number in params["subject_number"]:
            choice = {
                "subject": sentence_object["subject"],
                "verb": sentence_object["verb"],
                "object": sentence_object["object"],
                "subject_number": number, 
                "object_number": number,
                "tense": tense
            }
            choice_swapped = {
                "subject": sentence_object["object"],
                "verb": choice["verb"],
                "object": sentence_object["subject"],
                "subject_number": choice["subject_number"], 
                "object_number": choice["object_number"],
                "tense": choice["tense"]
            }
            make_choices.append(make_english_sentence(choice_swapped))
            make_choices.append(make_english_sentence(choice))
    return "\n".join(make_choices)

def identify(type_, params):
    for _ in range(random.randint(2,5)):
        if type_ is "word":
            # nouns or verbs
            word_type = random.choice(["nouns", "verbs"])
            # pick the word
            word = random.choice(params[word_type])

            print(word_type, word)
            
            # type dictionary... words ... generate a random correct answer depending on its type
            # pick a piece as the correct answer, highlight the random component
            # all choices for correct answer within parameters 
            # make latin prompt
            # return question_object (latin prompt + choices + correct answer)
	
def fill_in_the_blank(type_, params):
    return
def translate(type_, params):

    # Translate passages psuedo code...
    # random_nouns = random.sample(params["nouns"], 2)

    # sentence_object = {
    #     "subject": nouns_dictionary[random_nouns[0]],
    #     "verb": verbs_dictionary[random.choice(params["verbs"])],
    #     "object": nouns_dictionary[random_nouns[1]],
    #     "subject_number": random.choice(params["subject_number"]), 
    #     "object_number": random.choice(params["object_number"]),
    #     "tense": random.choice(params["tense"])
    # }

    # latin_sentence = make_latin_sentence(sentence_object)
    # print("=====")
    # print(latin_sentence)
    # print("\n")
    # choices = make_choices(sentence_object, params)
    # print(choices)

    # correct_answer_english = make_english_sentence(sentence_object)
    # print("\n")
    # print("answer:", correct_answer_english)
    # print("\n")

    return 

def generate_questions(params):
    print("===new level / new parameters in effect===")

    identify_words = identify("word", params)
    fill_in_the_blank_words = fill_in_the_blank("word", params)
    translate_words = translate("word", params)
    # print the questions for checking, TODO return question documents
    print(identify_words, fill_in_the_blank_words, translate_words)

    identify_passages = identify("passage", params)
    fill_in_the_blank_passages = fill_in_the_blank("passage", params)
    identify_words = translate("passage", params)
    # print the questions for checking, TODO return question documents
    print(identify_passages, fill_in_the_blank_passages, identify_words)

# set levels set in sequence.py
[generate_questions(params) for params in levels]
