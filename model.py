"""Models for recipeapp db"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """An app user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    starredrec = db.relationship("StarredRecipe")
    hashtag = db.relationship("Hashtag")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)


class Ingredient(db.Model):
    """An ingredient"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_name = db.Column(db.Unicode(64))

    recingr = db.relationship("RecipeIngredient")

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
    recipe_name = db.Column(db.Unicode(150))
    recipe_steps = db.Column(db.UnicodeText)

    starredrec = db.relationship("StarredRecipe")
    recingr = db.relationship("RecipeIngredient")
    reccat = db.relationship("RecipeCategory")
    hashtagization = db.relationship("Hashtagization")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_name=%s recipe_id=%s>" % (self.recipe_name,
                                                         self.recipe_id)


class Category(db.Model):
    """A recipe category"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(100))

    reccat = db.relationship("RecipeCategory")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Category category_name=%s category_id=%s>" %
                (self.category_name,
                 self.category_id
                 ))


class Unit(db.Model):
    """An ingredient unit"""

    __tablename__ = "units"

    unit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit_name = db.Column(db.String(64))

    recingr = db.relationship("RecipeIngredient")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Unit unit_name=%s unit_id=%s>" % (self.unit_name,
                                                   self.unit_id)


class Hashtag(db.Model):
    """A user-defined hashtag"""

    __tablename__ = "hashtags"

    hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    hashtag_name = db.Column(db.String(64))

    user = db.relationship("User")
    hashtagization = db.relationship("Hashtagization")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Hashtag hashtag_name=%s user_id=%s>" % (self.hashtag_name,
                                                         self.user_id,
                                                         )


class StarredRecipe(db.Model):
    """A recipe starred by a user"""

    __tablename__ = "starred_recipes"

    star_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    private = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.UnicodeText, nullable=True)
    has_made = db.Column(db.Boolean, default=False)

    user = db.relationship("User")
    recipe = db.relationship("Recipe")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<StarredRecipe id=%s user_id=%s recipe_id=%s>" %
                (self.star_id,
                 self.user_id,
                 self.recipe_id
                 ))


class RecipeIngredient(db.Model):
    """Middle table for recipe+ingredient pairing"""

    __tablename__ = "recipes_ingredients"

    rec_ingr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.ingredient_id"))
    quantity = db.Column(db.Float)
    unit_id = db.Column(db.Integer, db.ForeignKey("units.unit_id"))

    recipe = db.relationship("Recipe")
    ingredient = db.relationship("Ingredient")
    unit = db.relationship("Unit")

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
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))

    recipe = db.relationship("Recipe")
    category = db.relationship("Category")

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

    hashtagization_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey("hashtags.hashtag_id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))

    hashtag = db.relationship("Hashtag")
    recipe = db.relationship("Recipe")

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
