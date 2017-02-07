"""Utility file to seed recipeapp database"""

from model import connect_to_db, db
from model import User, Ingredient, Recipe, Category, Unit, Hashtag
from model import Starring, RecipeIngredient, RecipeCategory
from model import Hashtagization
from server import app


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

    db.session.add_all([Ingredient(ingredient_name='pasta'),
                        Ingredient(ingredient_name='cheese'),
                        Ingredient(ingredient_name='lettuce'),
                        Ingredient(ingredient_name='vinegar')
                        ])
    db.session.commit()


def load_recipes():
    """Load some sample recipes into database."""

    # delete all rows in the table
    Recipe.query.delete()

    db.session.add_all([Recipe(recipe_id=1, recipe_name='macaroni and cheese', recipe_steps="mix mac and cheese"),
                        Recipe(recipe_id=2, recipe_name='salad', recipe_steps="toss lettuce with vinegar")
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


def load_hashtags():
    """Load some sample hashtags into database."""

    # delete all rows in the table
    Hashtag.query.delete()

    db.session.add_all([Hashtag(hashtag_name='thanksgiving', user_id=1),
                        Hashtag(hashtag_name='thanksgiving', user_id=1),
                        Hashtag(hashtag_name='potluck', user_id=3),
                        Hashtag(hashtag_name='yas', user_id=1)
                        ])
    db.session.commit()


def load_starred_recipes():
    """Load some sample recipe starrings into database."""
    pass


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
    load_users()
    load_ingredients()
    load_recipes()
    load_categories()
    load_units()
    load_hashtags()
