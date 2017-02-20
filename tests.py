from server import *
from helpers import *
import unittest


class HelpersTestCase(unittest.TestCase):
    """Unit tests for helpers.py"""

    def test_string_space_to_plus(self):
        self.assertEqual(string_space_to_plus("my string"), "my+string")

    def test_string_space_to_plus_2(self):
        self.assertEqual(string_space_to_plus("mystring"), "mystring")

    def test_string_space_to_plus_3(self):
        self.assertEqual(string_space_to_plus("kentucky hot brown"), "kentucky+hot+brown")

    def test_parse_recipe_searchlist(self):
        self.assertEqual(parse_recipe_searchlist(["chinese", "japanese"]), "chinese%2C+japanese")
    # def test_adder_2(self):
    #     self.assertEqual(arithmetic.adder(2, 2), 4)

    # def test_things(self):
    #     self.assertEqual(len(arithmetic.things_from_db()), 3)


if __name__ == '__main__':
    # If called like a script, run my tests
    unittest.main()
