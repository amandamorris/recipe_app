from model import *


def parse_recipe_keywords(keyword_string):
    """Replace whitespace with + for recipe search api request"""
    return keyword_string.replace(" ", "+")


def parse_recipe_searchlist(searchlist):
    """Iterate through a list of search parameters and create a string to pass
    in the api request"""
    mystring = ""
    if len(searchlist):
        mystring = searchlist[0]
        for element in searchlist[1:]:
            mystring += "%2C+" + element
            # mystring += element
    return mystring


def add_recipe_to_db(json_response):
    """Parse json recipe and add new recipe to db"""
    """TODO: NEED TO MODIFY THIS FUNCTION TO ADD OTHER RECIPE INFO, LIKE
    INGREDIENTS, CUISINES, DIETS, IMAGES, ETC"""
    recipe_id = json_response['id']  # get recipe id from response
    recipe_name = json_response['title']  # get recipe name from response
    recipe_steps = json_response['instructions']  # get recipe instructions/steps
    if 'preparationMinutes' in json_response:
        recipe_active_time = json_response['preparationMinutes']
    else:
        recipe_active_time = None
    if 'readyInMinutes' in json_response:
        recipe_total_time = json_response['readyInMinutes']  # get cook time from response
    else:
        recipe_total_time = None
    recipe_servings = json_response['servings']  # get servings from response
    healthscore = json_response['healthScore']
    cheap = json_response['cheap']
    dairy_free = json_response['dairyFree']
    gluten_free = json_response['glutenFree']
    ketogenic = json_response['ketogenic']
    low_fodmap = json_response['lowFodmap']
    sustainable = json_response['sustainable']
    vegan = json_response['vegan']
    vegetarian = json_response['vegetarian']
    very_healthy = json_response['veryHealthy']
    very_popular = json_response['veryPopular']
    whole30 = json_response['whole30']

    recipe = Recipe(recipe_id=recipe_id,
                    recipe_name=recipe_name,
                    recipe_steps=recipe_steps,
                    recipe_total_time=recipe_total_time,
                    recipe_servings=recipe_servings,
                    recipe_active_time=recipe_active_time,
                    healthscore=healthscore,
                    cheap=cheap,
                    dairy_free=dairy_free,
                    gluten_free=gluten_free,
                    ketogenic=ketogenic,
                    low_fodmap=low_fodmap,
                    sustainable=sustainable,
                    vegan=vegan,
                    vegetarian=vegetarian,
                    very_healthy=very_healthy,
                    very_popular=very_popular,
                    whole30=whole30
                    )
    db.session.add(recipe)
    db.session.commit()


def add_recipe_properties_to_db(json_response):
    """Add recipe cuisines, dish types, images, to db"""
    recipe_id = json_response['id']
    dish_types = json_response['dishTypes']
    # if the recipe lists dish types...
    if dish_types:
        # check to see if the dish type is in the db, and if not, add it
        for dish_type in dish_types:
            if not DishType.query.get(dish_type):
                new_dish_type = DishType(dish_type_name=dish_type)
                db.session.add(new_dish_type)
                db.session.commit()
            # add a new recipe_dish_type for this recipe
            recipe_dish_type = RecipeDishType(recipe_id=recipe_id,
                                              dish_type_name=dish_type
                                              )
            db.session.add(recipe_dish_type)
            db.session.commit()


# def add_ingredients_to_db(json_response):
#     """Check for ingredients in db, and if not there, add them"""
#     for ingredient_dict in json_response['extendedIngredients']:
#         ingredient = Ingredient.query.filter_by(ingredient_name=ingredient_dict['name']).first()
#         if not ingredient:
#             print 'ingredient %s not in db' % (ingredient_dict['name'])
#         else:
#             print ingredient

def add_ingredients_to_db(json_response):
    """Check for ingredient_id, unit, recipe_ingredient in db, and add any that
    are not there"""

    for ingredient in json_response['extendedIngredients']:
        # check to see if ingredient is in db, and if not, add it
        db_ingredient = Ingredient.query.get(ingredient['id'])
        if not db_ingredient:
            new_ingredient = Ingredient(ingredient_id=ingredient['id'],
                                        ingredient_name=ingredient['name']
                                        )
            db.session.add(new_ingredient)
            db.session.commit()

        # check to see if unit is in the db, and if not, add it
        ingredient_unit = ingredient['unitLong']
        db_unit = Unit.query.get(ingredient_unit)
        if ingredient_unit and not db_unit:
            new_unit = Unit(unit_name=ingredient_unit)
            db.session.add(new_unit)
            db.session.commit()
        elif not ingredient_unit:
            ingredient_unit = None

        # check to see if recipeingredient is in the db, and if not, add it
        db_recipe_ingredient = RecipeIngredient.query.filter_by(recipe_id=json_response['id'], ingredient_id=ingredient['id']).first()
        if not db_recipe_ingredient:
            new_recipe_ingredient = RecipeIngredient(recipe_id=json_response['id'],
                                                     ingredient_id=ingredient['id'],
                                                     quantity=ingredient['amount'],
                                                     unit_name=ingredient_unit
                                                     )
            db.session.add(new_recipe_ingredient)
            db.session.commit()
# def add_recipe_ingredients_to_db(json_response):
#     """Add recipe ingredients to database"""
#     pass
