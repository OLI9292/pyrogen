import random
from linguistic_generator import *
from sequence import *

def format_question(word_object, choices, answer):
    formatted_prompt = "-".join(word_object["latin"].values())
    redHerrings = choices
    redHerrings.remove(answer)
    return {
        "redHerrings" : redHerrings,
        "prompt": [{"value": formatted_prompt}],
        "answer": answer
    }

def make_word_question(type_, params): 
    word = random.choice(params[type_])
    number = random.choice(params["number"])
    if type_ is "verbs":
        tense = random.choice(params["tense"])

        verb = verbs_dictionary[word]
        word_object = make_verb(verb, "subject", number, tense)

        answer_component = random.choice(list(word_object["latin"].items()))
        answer_tag = next(iter(answer_component))
        if answer_tag is "beginning":
            choices = [item for item in verbs_dictionary]
            answer = word
            word_object["latin"]["beginning"] = word_object["latin"]["beginning"].upper()
        elif answer_tag is "middle":
            choices = list(middle_elements_of_verbs.keys())
            answer = tense
            word_object["latin"]["middle"] = word_object["latin"]["middle"].upper()
        else:
            choices = [item for item in latin_verb_endings]
            answer = number
            word_object["latin"]["end"] = word_object["latin"]["end"].upper()

        return format_question(word_object, choices, answer)

    else:
        functions = ["subject", "object"]
        function = random.choice(functions)

        noun = nouns_dictionary[word]
        word_object = make_noun(noun, function, number)

        answer_component = random.choice(list(word_object["latin"].items()))
        answer_tag = next(iter(answer_component))
        if answer_tag is "beginning":
            choices = [item for item in nouns_dictionary]
            answer = word   
            word_object["latin"]["beginning"] = word_object["latin"]["beginning"].upper()
        else:
            choices = [function + " " + number for number in params["number"] for function in functions]
            answer = function + " " + number
            word_object["latin"]["end"] = word_object["latin"]["end"].upper()

        return format_question(word_object, choices, answer)

def identify(type_, params):
    if type_ is "word":
        word_type = random.choice(["nouns", "verbs"])
        return make_word_question(word_type, params)
    elif type_ is "sentence":
        #TODO Sentence Integration
        print("TODO sentence")
    else:
        print("invalid type entered")

def generate_questions(params):
    questions = []
    for _ in range(random.randint(4,7)):
       questions.append(identify("word", params))
    
        #TODO Other question types
        # fill_in_the_blank_words = fill_in_the_blank("word", params)
        # translate_words = translate("word", params)

        # questions.append(identify("sentence", params))
        # questions.append(fill_in_the_blank("sentence", params))
        # questions.append(translate("sentence", params))

    return questions

# set levels set in sequence.py
def sequence_output(iterations):
    import json
    counter = 0
    for idx in range(iterations):
        questions = []
        for level in levels:
            questions += generate_questions(level)
        with open("latin_test-sequence-" + str(idx) + '.json', 'w') as outfile:
            json.dump(questions, outfile)
        counter += len(questions)
    print("finished, total questions", counter)

sequence_output(20)