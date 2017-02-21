from server import *
from helpers import *
from model import *
import unittest


# class HelpersTestCase(unittest.TestCase):
#     """Unit tests for API calls and string manipulation in helpers.py"""

#     def setUp(self):
#         self.result = get_recipe_details_from_api("520083")
#         self.recipe_details = self.result.body
#         # server.app.config['TESTING'] = True
#         url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?diet=vegetarian&excludeIngredients=coconut&instructionsRequired=true&intolerances=tree+nut&limitLicense=false&number=10&offset=0&query=cauliflower&type=soup"
#         self.result1 = get_recipe_briefs_from_api(url)
#         self.recipe_briefs = self.result1.body


#     def test_string_space_to_plus(self):
#         self.assertEqual(string_space_to_plus("my string"), "my+string")

#     def test_string_space_to_plus_2(self):
#         self.assertEqual(string_space_to_plus("mystring"), "mystring")

#     def test_string_space_to_plus_3(self):
#         self.assertEqual(string_space_to_plus("kentucky hot brown"), "kentucky+hot+brown")

    
#     def test_parse_recipe_searchlist(self):
#         self.assertEqual(parse_recipe_searchlist(["chinese", "japanese"]), "chinese%2C+japanese")

#     def test_parse_recipe_searchlist_2(self):
#         self.assertEqual(parse_recipe_searchlist([]), "")


#     def test_get_recipe_details_from_api(self):
#         self.assertTrue(self.result.code == 200)

#     def test_get_recipe_details_from_api_1(self):
#         self.assertIsInstance(self.result, unirest.UnirestResponse)

#     def test_get_recipe_details_from_api_2(self):
#         self.assertTrue("extendedIngredients" in self.recipe_details)

#     def test_get_recipe_details_from_api_3(self):
#         self.assertTrue(self.recipe_details['id'] == 520083)


#     def test_get_recipe_briefs_from_api(self):
#         self.assertTrue(self.result1.code == 200)

#     def test_get_recipe_briefs_from_api_1(self):
#         self.assertIsInstance(self.result1, unirest.UnirestResponse)

#     def test_get_recipe_briefs_from_api_2(self):
#         self.assertTrue(len(self.recipe_briefs['results']) > 0)

# testdb = SQLAlchemy()

def connect_to_db(app, db_uri='postgresql:///testdb'):
    """Connect the database to my Flask app."""

    # Configure to use our PstgreSQL database

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


class HelpersDBTestCase(unittest.TestCase):
    """Unit tests for db updating functions in helpers.py"""

    def setUp(self):
        print "setting up"
        connect_to_db(app)

        self.client = app.test_client()
        app.config['TESTING'] = True
        # Connect to test database

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""
        print "tearing down"
        db.session.close()
        db.drop_all()

    def test_example(self):
        print "here's my test"

    def test_find_user(self):
        """Can we find a user in the sample data?"""

        balloon = User.query.filter(User.username == "balloon").first()
        self.assertEqual(balloon.username, "balloon")

    def test_user_recipes(self):
        """Can we get a user's recipes?"""
        balloon = User.query.filter(User.username == "balloon").first()
        basilcheese = Recipe.query.get(2)
        self.assertIn(basilcheese, balloon.recipes)


if __name__ == '__main__':
    # If called like a script, run my tests
    unittest.main()
