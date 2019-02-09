import sys
import unittest

from lib.helpers import find_path_in_dict

from db.mocks.conjugation import conjugation_mocks

english_conjugation = conjugation_mocks["english"][0]["data"]
latin_conjugation = conjugation_mocks["latin"][0]["data"]


class TestStringMethods(unittest.TestCase):

    def test_english_conjugation(self):
        keys = ["present", "singular", "3"]
        result = find_path_in_dict(keys, english_conjugation)
        self.assertEqual(result, "s")

        keys = ["past"]
        result = find_path_in_dict(keys, english_conjugation)
        self.assertEqual(result, "ed")

    def test_latin_conjugation(self):
        keys = ["present", "singular", "2"]
        result = find_path_in_dict(keys, latin_conjugation)
        self.assertEqual(result, "as")

        keys = ["past", "singular", "3"]
        result = find_path_in_dict(keys, latin_conjugation)
        self.assertEqual(result, "it")


if __name__ == '__main__':
    unittest.main()
