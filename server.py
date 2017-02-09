from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from jinja2 import StrictUndefined
from model import connect_to_db, db
from model import User, Recipe, Ingredient, Hashtag, Category, Unit
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

    # These code snippets use an open-source library. http://unirest.io/python
    return render_template("homepage.html")


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
        session['user'] = username
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
    """Recipes <username> tagged with <hashtag_name>"""
    # do request.args.get to get username and hashtag#
    username = request.args.get("username")  # the username
    my_hash = request.args.get("hashtag")  # the hashtag

    # user = User.query.get(user)  # the user object
    hashtag = db.session.query(Hashtag).filter((Hashtag.hashtag_name == my_hash) & (Hashtag.username == username)).first()
    # print "try2 %s %s" % (username, hashtag)
    recipes = hashtag.recipes
    # print recipes
    recipes_info = {}
    for recipe in recipes:
        recipe_dict = recipe.create_recipe_dictionary()
        recipes_info[recipe.recipe_name] = recipe_dict
        recipes_info[recipe.recipe_name]["hashtag"] = my_hash
        # recipes_info.append(recipe.create_recipe_dictionary())
        # recipes_info["hashtag"] = my_hash
        print recipes_info

    # list of dictionaries, but need a method in my class for getting a dictionary-like thing for a recipe
    # for recipe in recipes:
    #     recipe_info.add(recipe.recipe_name)

    return jsonify(recipes_info)


@app.route('/logout')
def logout():
    """Logout - remove user from session and redirect to homepage"""
    del session['user']
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


@app.route('/search_recipes')
def search_recipes():
    """Search recipes using keywords"""

    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?diet=vegetarian&excludeIngredients=coconut&instructionsRequired=false&intolerances=egg%2C+gluten&limitLicense=false&number=10&offset=0&query=kale&type=main+course",
                           headers={
                               "X-Mashape-Key": MASHAPE_KEY,
                               "Accept": "application/json"
                               }
                           )
    results = response.body
    print results
    return redirect('/')


@app.route('/show_recipe')
def show_recipe():
    """Display a recipe"""
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/479101/information?includeNutrition=false",
                           headers={
                               "X-Mashape-Key": MASHAPE_KEY,
                               "Accept": "application/json"
                               }
                           )
    recipe = response.body
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
