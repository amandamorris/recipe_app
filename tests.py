from server import *
from helpers import *
import unittest


class HelpersTestCase(unittest.TestCase):
    """Unit tests for helpers.py"""

    def setUp(self):
        self.result = get_recipe_details_from_api("520083")
        self.recipe_details = self.result.body
        # server.app.config['TESTING'] = True


    def test_string_space_to_plus(self):
        self.assertEqual(string_space_to_plus("my string"), "my+string")

    def test_string_space_to_plus_2(self):
        self.assertEqual(string_space_to_plus("mystring"), "mystring")

    def test_string_space_to_plus_3(self):
        self.assertEqual(string_space_to_plus("kentucky hot brown"), "kentucky+hot+brown")

    
    def test_parse_recipe_searchlist(self):
        self.assertEqual(parse_recipe_searchlist(["chinese", "japanese"]), "chinese%2C+japanese")

    def test_parse_recipe_searchlist_2(self):
        self.assertEqual(parse_recipe_searchlist([]), "")


    def test_get_recipe_details_from_api(self):
        self.assertTrue(self.result.code == 200)

    def test_get_recipe_details_from_api_1(self):
        self.assertIsInstance(self.result, unirest.UnirestResponse)

    def test_get_recipe_details_from_api_2(self):
        self.assertTrue("extendedIngredients" in self.recipe_details)

    def test_get_recipe_details_from_api_3(self):
        self.assertTrue(self.recipe_details['id'] == 520083)




if __name__ == '__main__':
    # If called like a script, run my tests
    unittest.main()
