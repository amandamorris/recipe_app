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
    recipe_active_time = db.Column(db.Integer)
    recipe_total_time = db.Column(db.Integer)
    recipe_servings = db.Column(db.Integer)
    healthscore = db.Column(db.Integer)
    cheap = db.Column(db.Boolean, default=False)
    dairy_free = db.Column(db.Boolean, default=False)
    gluten_free = db.Column(db.Boolean, default=False)
    ketogenic = db.Column(db.Boolean, default=False)
    low_fodmap = db.Column(db.Boolean, default=False)
    sustainable = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    vegetarian = db.Column(db.Boolean, default=False)
    very_healthy = db.Column(db.Boolean, default=False)
    very_popular = db.Column(db.Boolean, default=False)
    whole30 = db.Column(db.Boolean, default=False)

    users = db.relationship("User", secondary="starrings")
    dish_types = db.relationship("DishType", secondary="recipes_dish_types")
    ingredients = db.relationship("Ingredient", secondary="recipes_ingredients")
    hashtags = db.relationship("Hashtag", secondary="hashtagizations")
    starrings = db.relationship("Starring")
    images = db.relationship("Image")

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
        recipe['active_time'] = self.recipe_active_time
        recipe['total_time'] = self.recipe_total_time
        # recipe['ingredients'] = []
        ingrs = self.get_ingredient_list()
        recipe['ingredients'] = ingrs
        recipe['images'] = []
        for db_image in self.images:
          recipe['images'].append(db_image.image_url)

        return recipe


class DishType(db.Model):
    """A recipe dish type"""

    __tablename__ = "dish_types"

    dish_type_name = db.Column(db.String(100), primary_key=True)

    recipes = db.relationship("Recipe", secondary='recipes_dish_types')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Dish Type dish_type_name=%s >" % (self.dish_type_name))


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


class Image(db.Model):
    """A recipe image"""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )
    image_url = db.Column(db.UnicodeText)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Image image_id=%s recipe_id=%s" % (self.image_id,
                                                    self.recipe_id
                                                    )


class DietType(db.Model):
    """Dietary restrictions"""

    __tablename__ = "diet_types"

    diet_name = db.Column(db.UnicodeText, primary_key=True)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<DietType diet_name=%s" % (self.diet_name)


# TODO: finish this class
# class RecipeDietType(db.Model):
#     """Middle table for recipe+diet type pairings"""

#     __tablename__ = "recipes_diet_types"


class Cuisine(db.Model):
    """A recipe cuisine"""

    __tablename__ = "cuisines"

    cuisine_name = db.Column(db.UnicodeText, primary_key=True)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Cuisine cuisine_name=%s" % (self.cuisine_name)


class RecipeCuisine(db.Model):
    """Association table for recipe+cuisine pairing"""

    __tablename__ = "recipes_cuisines"

    recipe_cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )
    cuisine_name = db.Column(db.UnicodeText,
                             db.ForeignKey("cuisines.cuisine_name"),
                             nullable=False
                             )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<RecipeCuisine recipe_cuisine=%s recipe_id=%s cuisine_id=%s>" %
                (self.recipe_cuisine_id,
                 self.recipe_id,
                 self.cuisine_id
                 ))


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


class RecipeDishType(db.Model):
    """Association table for recipe+dish type pairings"""

    __tablename__ = "recipes_dish_types"
    rec_dish_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipes.recipe_id"),
                          nullable=False
                          )
    dish_type_name = db.Column(db.UnicodeText,
                               db.ForeignKey("dish_types.dish_type_name"),
                               nullable=False
                               )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<RecipeDishType rec_dish_type_id=%s recipe_id=%s dish_type_id=%s>" %
                (self.rec_dish_type_id,
                 self.recipe_id,
                 self.dish_type_id
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
def connect_to_db(app, db_uri="postgresql:///recipeapp"):
    """Connect the database to my Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    db.session.add_all([User(username='amanda', password='hi'),
                        User(username='balloon', password='icorn'),
                        User(username='honey', password='dew')
                        ])
    db.session.add_all([Ingredient(ingredient_name='pasta', ingredient_id=1),
                        Ingredient(ingredient_name='cheese', ingredient_id=2),
                        Ingredient(ingredient_name='basil', ingredient_id=3)
                        ])
    db.session.add_all([Recipe(recipe_id=1,
                               recipe_name='macaroni and cheese',
                               recipe_steps="mix mac and cheese",
                               recipe_total_time=30
                               ),
                        Recipe(recipe_id=2,
                               recipe_name="basil cheese",
                               recipe_steps="combine basil and cheese",
                               recipe_total_time=5
                               )
                        ])
    db.session.add_all([DishType(dish_type_name='appetizer'),
                        DishType(dish_type_name='entree')
                        ])
    db.session.add_all([Unit(unit_name='cup'),
                        Unit(unit_name='ounce')
                        ])
    db.session.commit()
    db.session.add_all([Hashtag(hashtag_name='thanksgiving', username='amanda'),
                        Hashtag(hashtag_name='christmas', username='balloon'),
                        Hashtag(hashtag_name='potluck', username='amanda'),
                        Hashtag(hashtag_name='potluck', username='honey')
                        ])
    db.session.add_all([Starring(recipe_id=1, username='amanda'),
                        Starring(recipe_id=2, username='balloon'),
                        Starring(recipe_id=1, username='amanda')
                        ])
    db.session.add_all([RecipeIngredient(recipe_id=1,
                                         ingredient_id=1,
                                         quantity=3.0,
                                         unit_name='cup'
                                         ),
                        RecipeIngredient(recipe_id=1,
                                         ingredient_id=2,
                                         quantity=0.5,
                                         unit_name='ounce'
                                         ),
                        RecipeIngredient(recipe_id=2,
                                         ingredient_id=2,
                                         quantity=4,
                                         unit_name='ounce'
                                         ),
                        RecipeIngredient(recipe_id=2,
                                         ingredient_id=3,
                                         quantity=.25,
                                         unit_name='cup'
                                         )
                        ])
    db.session.add_all([RecipeDishType(recipe_id=2, dish_type_name="appetizer"),
                        RecipeDishType(recipe_id=1, dish_type_name="entree"),
                        RecipeDishType(recipe_id=1, dish_type_name="appetizer")
                        ])
    db.session.commit()
    db.session.add_all([Hashtagization(hashtag_id=1, recipe_id=2),
                        Hashtagization(hashtag_id=2, recipe_id=2),
                        Hashtagization(hashtag_id=3, recipe_id=1)
                        ])

    db.session.commit()


if __name__ == "__main__":
    # If this module is run interactively, you will be able to work with the
    # database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
