import random
import itertools
import copy


def flatten(l):
    return [item for sublist in l for item in sublist]


def is_string(key, obj):
    try:
        return isinstance(obj[key], basestring)
    except:
        return False


def isinstance_of(entity, key, obj):
    try:
        return isinstance(obj[key], entity)
    except:
        return False


def find_path_in_dict(keys, obj):
    combination_tuples = [list(itertools.combinations(keys, l + 1))
                          for l in range(len(keys))]
    combination_lists = [list(t)
                         for t in reversed(flatten(combination_tuples))]

    for combination in combination_lists:
        direct_key = " ".join(combination)

        if direct_key in obj:
            if isinstance_of(basestring, direct_key, obj):
                return obj[direct_key]
            if isinstance_of(list, direct_key, obj):
                return random.choice(obj[direct_key])

        copy_obj = copy.deepcopy(obj)

        while len(combination) > 0:
            key = combination.pop(0)
            if key in copy_obj:
                if isinstance_of(basestring, key, copy_obj):
                    return copy_obj[key]
                else:
                    copy_obj = copy_obj[key]

    return ""
