"""Models for recipeapp db"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """An app user"""

    __tablename__ = "users"

    username = db.Column(db.String(64), primary_key=True)
    # username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    recipes = db.relationship("Recipe", secondary="starrings")  # look at this to doublecheck
    hashtags = db.relationship("Hashtag")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User username=%s>" % (self.username)


class Ingredient(db.Model):
    """An ingredient"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.Unicode(64), nullable=False)

    recipes = db.relationship("Recipe", secondary="recipes_ingredients")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Ingredient ingredient_name=%s ingredient_id=%s>" %
                (self.ingredient_name,
                 self.ingredient_id
                 ))


class Recipe(db.Model):
    """A recipe"""

    __tablename__ = "recipes"

# TODO: check spoonacular's API to see what type the recipe ids are
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.Unicode(150), nullable=False)
    recipe_steps = db.Column(db.UnicodeText, nullable=False)
    recipe_time = db.Column(db.Integer, nullable=False)

    users = db.relationship("User", secondary="starrings")
    categories = db.relationship("Category", secondary="recipes_categories")
    ingredients = db.relationship("Ingredient", secondary="recipes_ingredients")
    hashtags = db.relationship("Hashtag", secondary="hashtagizations")
    starrings = db.relationship("Starring")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_name=%s recipe_id=%s>" % (self.recipe_name,
                                                         self.recipe_id)

    def get_ingredient_list(self):
        """Write a function to get a list of ingredients with quantities and
        units, for a recipe
        """
        rec_ingrs_info = []
        for ingredient in self.ingredients:
            ingr_info = {}
            ingr_info['ingredient_id'] = ingredient.ingredient_id
            ingr_info['ingredient_name'] = ingredient.ingredient_name
            qty = db.session.query(RecipeIngredient.quantity).filter(
                (RecipeIngredient.recipe_id == self.recipe_id) & (RecipeIngredient.ingredient_id == ingredient.ingredient_id)).first()
            ingr_info['quantity'] = qty[0]
            unit = db.session.query(RecipeIngredient.unit_name).filter(
                (RecipeIngredient.recipe_id == self.recipe_id) & (RecipeIngredient.ingredient_id == ingredient.ingredient_id)).first()
            ingr_info['unit'] = unit[0]
            rec_ingrs_info.append(ingr_info)
        return rec_ingrs_info

    def create_recipe_dictionary(self):
        """Create a dictionary of recipe+ingredient info, for jsonification"""

        recipe = {}

        recipe['recipe_id'] = self.recipe_id
        recipe['recipe_name'] = self.recipe_name
        recipe['steps'] = self.recipe_steps
        recipe['time'] = self.recipe_time
        recipe['ingredients'] = []
        ingrs = self.get_ingredient_list()
        recipe['ingredients'] = ingrs

        return recipe


class Category(db.Model):
    """A recipe category"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)

    recipes = db.relationship("Recipe", secondary='recipes_categories')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Category category_name=%s category_id=%s>" %
                (self.category_name,
                 self.category_id
                 ))


class Unit(db.Model):
    """An ingredient unit"""

    __tablename__ = "units"

    unit_name = db.Column(db.String(64), primary_key=True)
    # unit_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Unit unit_name=%s>" % (self.unit_name)


class Hashtag(db.Model):
    """A user-defined hashtag"""

    __tablename__ = "hashtags"

    hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64),
                         db.ForeignKey("users.username"),
                         nullable=False
                         )
    hashtag_name = db.Column(db.String(64), nullable=False)

    user = db.relationship("User")
    recipes = db.relationship("Recipe", secondary="hashtagizations")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Hashtag hashtag_name=%s username=%s>" % (self.hashtag_name,
                                                         self.username,
                                                         )


class Starring(db.Model):
    """A starring of a recipe by a user"""

    __tablename__ = "starrings"

    star_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )
    username = db.Column(db.String(64),
                         db.ForeignKey("users.username"),
                         nullable=False
                         )
    private = db.Column(db.Boolean, default=True, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.UnicodeText, nullable=True)
    has_made = db.Column(db.Boolean, default=False, nullable=False)

    # recipe = db.relationship("Recipe")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Starring id=%s username=%s recipe_id=%s>" %
                (self.star_id,
                 self.username,
                 self.recipe_id
                 ))


class RecipeIngredient(db.Model):
    """Middle table for recipe+ingredient pairing"""

    __tablename__ = "recipes_ingredients"

    rec_ingr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey("ingredients.ingredient_id"),
                              nullable=False
                              )
    quantity = db.Column(db.Float)
    unit_name = db.Column(db.String(64), db.ForeignKey("units.unit_name"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<RecipeIngredient rec_ingr_id=%s recipe_id=%s ingredient_id=%s>" %
                (self.rec_ingr_id,
                 self.recipe_id,
                 self.ingredient_id
                 ))


class RecipeCategory(db.Model):
    """Association table for recipe+category pairings"""

    __tablename__ = "recipes_categories"

    rec_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )
    category_id = db.Column(db.Integer,
                            db.ForeignKey("categories.category_id"),
                            nullable=False
                            )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<RecipeCategory rec_cat_id=%s recipe_id=%s category_id=%s>" %
                (self.rec_cat_id,
                 self.recipe_id,
                 self.category_id
                 ))


class Hashtagization(db.Model):
    """Association table for hashtag+recipe pairings"""

    __tablename__ = "hashtagizations"

    hashtagization_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True
                                  )
    hashtag_id = db.Column(db.Integer,
                           db.ForeignKey("hashtags.hashtag_id"),
                           nullable=False
                           )
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<#-ization #-ization_id=%s #_id=%s recipe_id=%s>" %
                (self.hashtagization_id,
                 self.hashtag_id,
                 self.recipe_id,
                 ))


##### Helper functions #####
def connect_to_db(app):
    """Connect the database to my Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipeapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If this module is run interactively, you will be able to work with the
    # database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
