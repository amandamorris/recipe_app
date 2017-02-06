"""Models for recipeapp db"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """An app user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)


class Ingredient(db.Model):
    """An ingredient"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_name = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ingredient_name=%s ingredient_id=%s>" % (self.ingredient_name,
                                                                     self.ingredient_id)


class Recipe(db.Model):
    """A recipe"""

    __tablename__ = "recipes"

# TODO: check spoonacular's API to see what type the recipe ids are
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(150))
    recipe_steps = db.Column(db.String(2000))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_name=%s recipe_id=%s>" % (self.recipe_name,
                                                         self.recipe_id)

# class Category(db.Model):
#     """A recipe category"""

#     __tablename__ = "categories"
#     pass

# class Unit(db.Model):
#     """An ingredient unit"""

#     __tablename__ = "units"
#     pass

# class StarredRecipe(db.Model):
#     """A recipe starred by a user"""

#     __tablename__ = "starred_recipes"
#     pass

# class Hashtag(db.Model):
#     """A user-defined hashtag"""

#     __tablename__ = "hashtags"
#     pass

# class RecipeIngredient(db.Model):
#     """A recipe+ingredient pairing"""

#     __tablename__ = "recipes_ingredients"
#     pass

# class RecipeCategory(db.Model):
#     """A recipe+category pairing"""

#     __tablename__ = "recipes_categories"
#     pass

# class Hashtagization(db.Model):
#     """A hashtag+recipe pairing"""

#     __tablename__ = "hashtagizations"
#     pass


##### Helper functions #####
def connect_to_db(app):
    """Connect the database to my Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipeapp'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If this module is run interactively, you will be able to work with the
    # database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
