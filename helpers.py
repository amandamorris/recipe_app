from model import *
import unirest


def get_recipe_briefs_from_api(url):
    """Make an API call to Spoonacular to see recipe search results"""

    response = unirest.get(url,
                           headers={
                               "X-Mashape-Key": "wa0SHrWJ0RmshsmbMjqSjVvrUEWpp1YiqdujsnXNFScqFYHcjq",
                               "Accept": "application/json"
                               }
                           )
    return response


def get_recipe_details_from_api(recipe_id):
    """Make an API call to Spoonacular to get recipe info"""

    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
                           + recipe_id + "/information?includeNutrition=false",
                           headers={"X-Mashape-Key": "wa0SHrWJ0RmshsmbMjqSjVvrUEWpp1YiqdujsnXNFScqFYHcjq",
                                    "Accept": "application/json"
                                    }
                           )
    return response


def string_space_to_plus(keyword_string):
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


def add_starring_to_db(username, recipe_id):
    """Add recipe starring to database"""

    new_starring = Starring(recipe_id=recipe_id,
                            username=username
                            )
    db.session.add(new_starring)
    db.session.commit()


def add_recipe_to_db(json_response):
    """Parse json recipe and add new recipe to db"""

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
    # if the recipe lists dish types...
    if 'dishTypes' in json_response:
        dish_types = json_response['dishTypes']
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
    # if the recipe lists cuisines...
    if 'cuisines' in json_response:
        cuisines = json_response['cuisines']
        # check to see if each cuisine is in the db, and if not, add it
        for cuisine in cuisines:
            if not Cuisine.query.get(cuisine):
                new_cuisine = Cuisine(cuisine_name=cuisine)
                db.session.add(new_cuisine)
                db.session.commit()
            # add a new recipe_cuisine pairing for each cuisine
            recipe_cuisine = RecipeCuisine(recipe_id=recipe_id,
                                           cuisine_name=cuisine
                                           )
            db.session.add(recipe_cuisine)
            db.session.commit()
    # if the recipe contains images, see if they're in the db and if not, add
    if 'image' in json_response:
        image_url = json_response['image']
        if not Image.query.filter_by(recipe_id=recipe_id, image_url=image_url).first():
            new_image = Image(recipe_id=recipe_id,
                              image_url=image_url
                              )
            db.session.add(new_image)
            db.session.commit()


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
