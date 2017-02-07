"""Models for recipeapp db"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """An app user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    starrings = db.relationship("Starring")
    hashtags = db.relationship("Hashtag")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)


class Ingredient(db.Model):
    """An ingredient"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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

    def get_ingredients_and_quantiities(self):
        """Write a function to get a list of ingredients with quantities,
        for a recipe
        #TODO
        """

#         >>> db.session.query(Ingredient, RecipeIngredient.quantity, Unit.unit_name).join(RecipeIngredient).join(Unit).filter(RecipeIngredient.recipe_id==recipe.recipe_id).all()
# [(<Ingredient ingredient_name=lettuce ingredient_id=3>, 3.0, u'cup'), (<Ingredient ingredient_name=pasta ingredient_id=1>, 0.5, u'ounce'), (<Ingredient ingredient_name=cheese ingredient_id=2>, 4.0, u'pound')]
        pass


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

    unit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Unit unit_name=%s unit_id=%s>" % (self.unit_name,
                                                   self.unit_id)


class Hashtag(db.Model):
    """A user-defined hashtag"""

    __tablename__ = "hashtags"

    hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False
                        )
    hashtag_name = db.Column(db.String(64), nullable=False)

    user = db.relationship("User")
    recipes = db.relationship("Recipe", secondary="hashtagizations")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Hashtag hashtag_name=%s user_id=%s>" % (self.hashtag_name,
                                                         self.user_id,
                                                         )


class Starring(db.Model):
    """A starring of a recipe by a user"""

    __tablename__ = "starrings"

    star_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False
                        )
    private = db.Column(db.Boolean, default=True, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.UnicodeText, nullable=True)
    has_made = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Starring id=%s user_id=%s recipe_id=%s>" %
                (self.star_id,
                 self.user_id,
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
    unit_id = db.Column(db.Integer, db.ForeignKey("units.unit_id"))

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
