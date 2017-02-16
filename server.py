from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from jinja2 import StrictUndefined
from model import connect_to_db, db
from model import User, Recipe, Ingredient, Hashtag, DishType, Unit
from helpers import *
import sqlalchemy
import unirest
import os


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "mysecretkey"

# If I use an undefined variable in Jinja2, raise an error.
app.jinja_env.undefined = StrictUndefined
MASHAPE_KEY = os.environ["MASHAPE_KEY"]


@app.route('/')
def index():
    """Homepage."""
    cuisine_types = Cuisine.query.filter().all()
    dish_types = DishType.query.filter().all()
    return render_template("homepage.html",
                           cuisine_types=cuisine_types,
                           dish_types=dish_types
                           )


@app.route('/login')
def login():
    """Login"""
    return render_template("login.html")


@app.route('/process_login', methods=['POST'])
def process_login():
    """Check if username/password combo is valid, and if so, login"""

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter(User.username == username).first()

    if user and user.password == password:
        session['username'] = username
        flash("You have successfully logged in")
        return redirect("/users/" + str(user.username))
    else:
        flash("Incorrect username/password combination.  Please try again or Register to create a new account")
        return redirect('/login')


@app.route('/users/<username>')
def users(username):
    """A user's info page"""
    user = User.query.get(username)

    return render_template("user.html", user=user)


@app.route('/user-hashtag-recipes.json')
def user_hashtag():
    """Recipes username tagged, by hashtag"""

    username = session['username']
    hashtag_list = User.query.get(username).hashtags

    recipes_by_hashtag = {}
    for hashtag in hashtag_list:
        recipes = hashtag.recipes
        recipes_info = {}
        for recipe in recipes:
            recipe_dict = recipe.create_recipe_dictionary()
            recipes_info[recipe.recipe_name] = recipe_dict
        recipes_by_hashtag[hashtag.hashtag_name] = recipes_info


    return jsonify(recipes_by_hashtag)


@app.route('/recipe_search')
def search_recipes():
    """Parse html recipe search form to create request to search api for recipes"""

    # save user's search parameters
    keywords = request.args.get("keywords")
    diet_type = request.args.get("diet_type")
    cuisine_types = request.args.getlist("cuisine")
    intolerances = request.args.getlist("intolerance")
    dish_type = request.args.get("dish_type")

    # base url
    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&number=10"

    # add search parameters to url, replacing space with +, and parsing out lists
    if keywords:
        url += "&query=" + string_space_to_plus(keywords)
    if intolerances:
        url += "&intolerances=" + string_space_to_plus(parse_recipe_searchlist(intolerances))
    if cuisine_types:
        url += "&cuisine=" + string_space_to_plus(parse_recipe_searchlist(cuisine_types))
    if diet_type:
        url += "&diet=" + diet_type
    if dish_type:
        url += "&type=" + string_space_to_plus(dish_type)

    # get search results from spoonacular api
    response = get_recipe_briefs_from_api(url)

    return render_template("search_results.html", response=response.body)


@app.route('/view_recipe.json', methods=['POST'])
def view_recipe():
    """Check if a recipe is in the db, and if not, add it,
    and either way, then display info from db"""

    recipe_id = request.form.get("recipe_id")
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    if not recipe:
        response = get_recipe_details_from_api(recipe_id)
        recipe_json = response.body

        # add all recipe info to database
        add_recipe_to_db(recipe_json)
        add_ingredients_to_db(recipe_json)
        add_recipe_properties_to_db(recipe_json)
        recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    recipe = recipe.create_recipe_dictionary()

    return jsonify(recipe)


@app.route('/star_recipe.json', methods=['POST'])
def star_recipe():
    """Add a user starring to the db, if it's not already there"""
    username = session['username']
    recipe_id = request.form.get("recipe_id")
    add_starring_to_db(username, recipe_id)
    return "{star: star}"

@app.route('/logout')
def logout():
    """Logout - remove user from session and redirect to homepage"""
    del session['username']
    flash("You have successfully logged out")

    return redirect('/')


@app.route('/register')
def register():
    """Register"""
    return render_template("register.html")


@app.route('/process_registration', methods=['POST'])
def process_registration():
    """Check if the given username is in the database, and if not, add it"""

    username = request.form.get("username")
    password = request.form.get("password")

    if User.query.filter(User.username == username).first():
        flash("User already exists - please login or try a different username")
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        session['user'] = username
        flash("You have successfully created an account and are now logged in")

    return redirect('/')



if __name__ == "__main__":
    # Set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
