"""Utility file to seed recipeapp database"""

from model import connect_to_db, db
from model import User, Ingredient, Recipe, Category, Unit, Hashtag
from model import Starring, RecipeIngredient, RecipeCategory
from model import Hashtagization
from server import app
import json


def get_response():
    response = {
      "servings": 10,
      "sourceUrl": "http://www.epicurious.com/recipes/food/views/Char-Grilled-Beef-Tenderloin-with-Three-Herb-Chimichurri-235342",
      "spoonacularSourceUrl": "https://spoonacular.com/char-grilled-beef-tenderloin-with-three-herb-chimichurri-156992",
      "aggregateLikes": 0,
      "creditText": "Epicurious",
      "sourceName": "Epicurious",
      "extendedIngredients": [
        {
          "id": 1022009,
          "aisle": "Ethnic Foods",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/chili-powder.jpg",
          "name": "ancho chile powder",
          "amount": 1.5,
          "unit": "teaspoons",
          "unitShort": "t",
          "unitLong": "teaspoons",
          "originalString": "1 1/2 teaspoons chipotle chile powder or ancho chile powder",
          "metaInformation": []
        },
        {
          "id": 13926,
          "aisle": "Meat",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/beef-tenderloin.jpg",
          "name": "beef tenderloin",
          "amount": 3.5,
          "unit": "pound",
          "unitShort": "lb",
          "unitLong": "pounds",
          "originalString": "1 3 1/2-pound beef tenderloin",
          "metaInformation": []
        },
        {
          "id": 1002030,
          "aisle": "Spices and Seasonings",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/pepper.jpg",
          "name": "black pepper",
          "amount": 0.5,
          "unit": "teaspoon",
          "unitShort": "t",
          "unitLong": "teaspoons",
          "originalString": "1/2 teaspoon freshly ground black pepper",
          "metaInformation": [
            "black",
            "freshly ground"
          ]
        },
        {
          "id": 1082047,
          "aisle": "Spices and Seasonings",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/salt.jpg",
          "name": "coarse kosher salt",
          "amount": 1,
          "unit": "tablespoon",
          "unitShort": "T",
          "unitLong": "tablespoon",
          "originalString": "1 tablespoon coarse kosher salt",
          "metaInformation": []
        },
        {
          "id": 10019334,
          "aisle": "Baking",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/brown-sugar-dark.jpg",
          "name": "dark brown sugar",
          "amount": 2,
          "unit": "tablespoons",
          "unitShort": "T",
          "unitLong": "tablespoons",
          "originalString": "2 tablespoons dark brown sugar",
          "metaInformation": [
            "dark"
          ]
        },
        {
          "id": 11165,
          "aisle": "Produce",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/cilantro.png",
          "name": "fresh cilantro",
          "amount": 2,
          "unit": "cups",
          "unitShort": "c",
          "unitLong": "cups",
          "originalString": "2 cups (packed) stemmed fresh cilantro",
          "metaInformation": [
            "fresh",
            "packed",
            "stemmed",
            "()"
          ]
        },
        {
          "id": 2064,
          "aisle": "Produce",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/mint.jpg",
          "name": "fresh mint",
          "amount": 1,
          "unit": "cup",
          "unitShort": "c",
          "unitLong": "cup",
          "originalString": "1 cup (packed) stemmed fresh mint",
          "metaInformation": [
            "fresh",
            "packed",
            "stemmed",
            "()"
          ]
        },
        {
          "id": 11297,
          "aisle": "Produce",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/parsley.jpg",
          "name": "fresh parsley",
          "amount": 3,
          "unit": "cups",
          "unitShort": "c",
          "unitLong": "cups",
          "originalString": "3 cups (packed) stemmed fresh parsley",
          "metaInformation": [
            "fresh",
            "packed",
            "stemmed",
            "()"
          ]
        },
        {
          "id": 11215,
          "aisle": "Produce",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/garlic.jpg",
          "name": "garlic cloves",
          "amount": 3,
          "unit": "",
          "unitShort": "",
          "unitLong": "",
          "originalString": "3 garlic cloves, peeled",
          "metaInformation": [
            "peeled"
          ]
        },
        {
          "id": 1002028,
          "aisle": "Spices and Seasonings",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/paprika.jpg",
          "name": "sweet paprika",
          "amount": 1,
          "unit": "tablespoon",
          "unitShort": "T",
          "unitLong": "tablespoon",
          "originalString": "1 tablespoon sweet smoked paprika*",
          "metaInformation": [
            "smoked"
          ]
        },
        {
          "id": 5,
          "aisle": "Spices and Seasonings",
          "image": "https://spoonacular.com/cdn/ingredients_100x100/paprika.jpg",
          "name": "my made up ingredient",
          "amount": 1,
          "unit": "tablespoon",
          "unitShort": "T",
          "unitLong": "tablespoon",
          "originalString": "1 tablespoon sweet smoked paprika*",
          "metaInformation": [
            "smoked"
          ]
        }
      ],
      "id": 156992,
      "title": "Char-Grilled Beef Tenderloin with Three-Herb Chimichurri",
      "readyInMinutes": 45,
      "image": "https://spoonacular.com/recipeImages/char-grilled-beef-tenderloin-with-three-herb-chimichurri-156992.jpg",
      "imageType": "jpg",
      "instructions": "PreparationFor spice rub:                                        Combine all ingredients in small bowl.                                                                            Do ahead: Can be made 2 days ahead. Store airtight at room temperature.                                    For chimichurri sauce:                                        Combine first 8 ingredients in blender; blend until almost smooth. Add 1/4 of parsley, 1/4 of cilantro, and 1/4 of mint; blend until incorporated. Add remaining herbs in 3 more additions, pureeing until almost smooth after each addition.                                                                            Do ahead: Can be made 3 hours ahead. Cover; chill.                                    For beef tenderloin:                                        Let beef stand at room temperature 1 hour.                                                                            Prepare barbecue (high heat). Pat beef dry with paper towels; brush with oil. Sprinkle all over with spice rub, using all of mixture (coating will be thick). Place beef on grill; sear 2 minutes on each side. Reduce heat to medium-high. Grill uncovered until instant-read thermometer inserted into thickest part of beef registers 130F for medium-rare, moving beef to cooler part of grill as needed to prevent burning, and turning occasionally, about 40 minutes. Transfer to platter; cover loosely with foil and let rest 15 minutes. Thinly slice beef crosswise. Serve with chimichurri sauce.                                                                            *Available at specialty foods stores and from tienda.com."
    }
    return response


def add_ingredients(response):
    """Parse a spoonacular json response and add ingredients to db if not already there"""
    # response = json.loads(response)

    ingreds = response["extendedIngredients"]  # get the list of ingredient dictionaries from response

    for ingredient_dict in ingreds:
        if not Ingredient.query.get(ingredient_dict['id']):  # if the ingredient isn't in the db, add it
            new_ingredient = Ingredient(ingredient_id=ingredient_dict['id'],
                                        ingredient_name=ingredient_dict['name']
                                        )
            db.session.add(new_ingredient)
    db.session.commit()


def add_recipe(response):
    recipe_id = response['id']  # get recipe id from response
    recipe_name = response['title']  # get recipe name from response
    recipe_steps = response['instructions']  # get recipe instructions/steps
    recipe_time = response['readyInMinutes']  # get cook time from response

    recipe = Recipe(recipe_id=recipe_id,
                    recipe_name=recipe_name,
                    recipe_steps=recipe_steps,
                    recipe_time=recipe_time
                    )
    db.session.add(recipe)
    db.session.commit()


def add_category(response):
    """Add category to db if not already there"""
    pass


def add_units(response):
    """Add units to db if not already there"""

    ingreds = response["extendedIngredients"]  # get the list of ingredient dictionaries from response
    for ingredient_dict in ingreds:
        if ingredient_dict['unit'] and not Unit.query.get(ingredient_dict['unit']):  # if the unit isn't in the db, add it
        # if ingredient_dict['unit'] and not Unit.query.filter(Unit.unit_name == ingredient_dict['unit']).first():
            new_unit = Unit(unit_name=ingredient_dict['unit'])
            db.session.add(new_unit)
    db.session.commit()


def add_recipe_ingredients(response):
    """Add recipe-ingredient pairings to the database"""

    ingreds = response["extendedIngredients"]  # get list of ingredients dictionaries
    recipe_id = response['id']  # get recipe id

    for ingredient_dict in ingreds:  # loop through ingredient dictionaries, and grab
        quantity = ingredient_dict['amount']  # quantity
        ingredient_id = ingredient_dict['id']  # ingredient id
        if ingredient_dict['unit']:
            unit_name = ingredient_dict['unit']
        else:
            unit_name = None
        # unit_id = db.session.query(Unit.unit_id).filter(Unit.unit_name == ingredient_dict['unit']).first()  # unit_id

        my_rec_ingr = RecipeIngredient(recipe_id=recipe_id,
                                       ingredient_id=ingredient_id,
                                       quantity=quantity,
                                       unit_name=unit_name
                                       )
        db.session.add(my_rec_ingr)
    db.session.commit()


def load_users():
    """Load some sample users into database."""

    # delete all rows in the table
    User.query.delete()

    db.session.add_all([User(username='amanda', password='hi'),
                        User(username='balloon', password='icorn'),
                        User(username='honey', password='dew')
                        ])
    db.session.commit()


def load_ingredients():
    """Load some sample ingredients into database."""

    # delete all rows in the table
    Ingredient.query.delete()

    db.session.add_all([Ingredient(ingredient_name='pasta', ingredient_id=1),
                        Ingredient(ingredient_name='cheese', ingredient_id=2),
                        Ingredient(ingredient_name='lettuce', ingredient_id=3),
                        Ingredient(ingredient_name='vinegar', ingredient_id=4),
                        Ingredient(ingredient_name='broccoli', ingredient_id=6)
                        ])
    db.session.commit()


def load_recipes():
    """Load some sample recipes into database."""

    # delete all rows in the table
    Recipe.query.delete()

    db.session.add_all([Recipe(recipe_id=1, recipe_name='macaroni and cheese', recipe_steps="mix mac and cheese", recipe_time=30),
                        Recipe(recipe_id=2, recipe_name='salad', recipe_steps="toss lettuce with vinegar", recipe_time=10),
                        Recipe(recipe_id=3, recipe_name='icewater', recipe_steps="take water, add ice", recipe_time=2)
                        ])
    db.session.commit()


def load_categories():
    """Load some sample categories into database."""

    # delete all rows in the table
    Category.query.delete()

    db.session.add_all([Category(category_name='appetizer'),
                        Category(category_name='entree'),
                        Category(category_name='dessert'),
                        Category(category_name='vegetarian')
                        ])
    db.session.commit()


def load_units():
    """Load some sample ingredient units into database."""

    # delete all rows in the table
    Unit.query.delete()

    db.session.add_all([Unit(unit_name='cup'),
                        Unit(unit_name='ounce'),
                        Unit(unit_name='pound'),
                        Unit(unit_name='can'),
                        Unit(unit_name='dash'),
                        ])


# def load_hashtags():
#     # TODO: need to tweak this so it's compatible with new unit_name primary key

#     """Load some sample hashtags into database."""

#     # delete all rows in the table
#     Hashtag.query.delete()

#     db.session.add_all([Hashtag(hashtag_name='thanksgiving', user_id=1),
#                         Hashtag(hashtag_name='thanksgiving', user_id=2),
#                         Hashtag(hashtag_name='potluck', user_id=3),
#                         Hashtag(hashtag_name='yas', user_id=1)
#                         ])
#     db.session.commit()


# def load_starrings():
#     # TODO: need to tweak this so it's compatible with new unit_name primary key

#     """Load some sample recipe starrings into database."""

#     # delete all rows in the table
#     Starring.query.delete()

#     db.session.add_all([Starring(recipe_id=1, user_id=2),
#                         Starring(recipe_id=2, user_id=2),
#                         Starring(recipe_id=2, user_id=3),
#                         Starring(recipe_id=2, user_id=1)
#                         ])
#     db.session.commit()


# def load_recipes_ingredients():
# # TODO: need to tweak this so it's compatible with new unit_name primary key
#     """Load some sample recipe-ingredients into database."""

#     # delete all rows in the table
#     RecipeIngredient.query.delete()

#     db.session.add_all([RecipeIngredient(recipe_id=1,
#                                          ingredient_id=3,
#                                          quantity=3.0,
#                                          unit_id=1
#                                          ),
#                         RecipeIngredient(recipe_id=2,
#                                          ingredient_id=1,
#                                          quantity=0.5,
#                                          unit_id=2
#                                          ),
#                         RecipeIngredient(recipe_id=1,
#                                          ingredient_id=2,
#                                          quantity=4,
#                                          unit_id=3
#                                          )
#                         ])


def load_recipes_categories():
    """Load some sample recipe-categorizations into database."""

    # delete all rows in the table
    RecipeCategory.query.delete()

    db.session.add_all([RecipeCategory(recipe_id=2, category_id=1),
                        RecipeCategory(recipe_id=1, category_id=1),
                        RecipeCategory(recipe_id=1, category_id=3),
                        RecipeCategory(recipe_id=1, category_id=4)
                        ])
    db.session.commit()


def load_hashtagizations():
    """Load some sample hashtagizations into database."""

    # delete all rows in the table
    Hashtagization.query.delete()

    db.session.add_all([Hashtagization(hashtag_id=1, recipe_id=2),
                        Hashtagization(hashtag_id=2, recipe_id=2),
                        Hashtagization(hashtag_id=3, recipe_id=1)
                        ])
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    response = get_response()
    add_ingredients(response)
    add_recipe(response)
    add_units(response)
    add_recipe_ingredients(response)

    # load_users()
    # load_ingredients()
    # load_recipes()
    # load_categories()
    # load_units()
    # load_hashtags()
    # load_starrings()
    # load_recipes_ingredients()
    # load_recipes_categories()
    # load_hashtagizations()
