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
    recipe_total_time = json_response['readyInMinutes']  # get cook time from response
    # recipe_active_time = response['']

    recipe = Recipe(recipe_id=recipe_id,
                    recipe_name=recipe_name,
                    recipe_steps=recipe_steps,
                    recipe_total_time=recipe_total_time
                    # recipe_active_time=recipe_active_time
                    )
    db.session.add(recipe)
    db.session.commit()
