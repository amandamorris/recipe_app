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

# Do I use this route???
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
    response = get_recipe_briefs_from_api(url).body
    hashtags = []
    if 'username' in session:
        username = session['username']
        hashtags = User.query.get(username).hashtags
        for recipe in response['results']:
            if not recipe_in_db(recipe['id']):
                get_recipe_and_add_to_db(recipe['id'])
            tags = get_recipe_hashtags(recipe['id'], username)
            recipe['tags'] = tags

        # hashtagizations = username.hashtags

    return render_template("search_results.html",
                           response=response,
                           hashtags=hashtags
                           )


@app.route('/view_recipe.json', methods=['POST'])
def view_recipe():
    """Check if a recipe is in the db, and if not, add it,
    and either way, then display info from db"""

    recipe_id = request.form.get("recipe_id")
    if not recipe_in_db(recipe_id):
        # make api call, add all recipe info to db
        get_recipe_and_add_to_db(recipe_id)
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    recipe = recipe.create_recipe_dictionary()

    for ingredient in recipe['ingredients']:
        quantity = str(ingredient['quantity'])
        ingredient['quantity'] = format_dec_as_frac(quantity)

    # if logged in, check to see if the user has already starred the recipe
    if 'username' in session:
        username = session['username']
    else:
        username = None
    if Starring.query.filter_by(username=username, recipe_id=recipe_id).first():
        is_starring = "true"
    else:
        is_starring = "false"
    recipe['is_starring'] = is_starring

    return jsonify(recipe)


@app.route('/star_recipe.json', methods=['POST'])
def star_recipe():
    """Add a user starring to the db, if it's not already there"""
    username = session['username']
    recipe_id = request.form.get("recipe_id")
    add_starring_to_db(username, recipe_id)
    print "starred"
    return "{star: star}"


@app.route('/display_hashed_recipes.json', methods=['GET'])
def display_hashed_recipes():
    """For each hashtag a user has created, show their hashed recipes"""
    print "display hashed recipes"
    username = session['username']
    hashtags = User.query.get(username).hashtags
    hashed_recipes = {}

    for db_hashtag in hashtags:
        hashtag_id = db_hashtag.hashtag_id
        hashtag_name = db_hashtag.hashtag_name
        hashed_recipes[hashtag_name] = get_hashtag_recipes(hashtag_id)


    return jsonify(hashed_recipes)

@app.route('/add_hashtag.json', methods=['POST'])
def add_hashtag():
    """Add a hashtag/user pair to the database"""
    username = session['username']
    hashtag_name = request.form.get("hashtag_name")
    print hashtag_name
    recipe_id = request.form.get("recipe_id")

    if not recipe_in_db(recipe_id):
        get_recipe_and_add_to_db(recipe_id)

    add_hashtag_to_db(username=username, hashtag_name=hashtag_name)

    db_hashtag = Hashtag.query.filter_by(hashtag_name=hashtag_name,
                                         username=username).first()
    hashtag_id = db_hashtag.hashtag_id

    add_hashtagization_to_db(recipe_id=recipe_id, hashtag_id=hashtag_id)

    return jsonify({"hashtag_name": hashtag_name, "recipe_id": recipe_id})


@app.route('/del_hashtagization.json', methods=['POST'])
def del_hashtagization():
    """Remove a hashtagization from the db"""
    username = session['username']
    hashtag_name = request.form.get("hashtag_name")
    recipe_id = request.form.get("recipe_id")

    # get the row corresponding to the hashtagization
    db_hashtagization = db.session.query(Hashtag).join(Hashtagization).filter(Hashtag.hashtag_name == hashtag_name,
                                                                              Hashtag.username == username).first()
    # from there, get the hashtag id
    hashtag_id = db_hashtagization.hashtag_id

    # delete the hastag from the db
    remove_hashtagization_from_db(hashtag_id=hashtag_id,
                                  recipe_id=recipe_id
                                  )
    # fetch updated hashtag list from db
    recipe_hashtags = get_recipe_hashtags(recipe_id=recipe_id, username=username)
    return jsonify({"hashtags": recipe_hashtags, "recipe_id": recipe_id})


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
