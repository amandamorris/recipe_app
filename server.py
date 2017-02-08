from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from jinja2 import StrictUndefined
from model import connect_to_db
from model import User, Recipe, Ingredient
import sqlalchemy


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "mysecretkey"

# If I use an undefined variable in Jinja2, raise an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

# # These code snippets use an open-source library.
# response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/479101/information?includeNutrition=false",
#   headers={
#     "X-Mashape-Key": "wa0SHrWJ0RmshsmbMjqSjVvrUEWpp1YiqdujsnXNFScqFYHcjq",
#     "Accept": "application/json"
#   }
# )


@app.route('/login')
def login():
    """Login"""
    pass


@app.route('/register')
def register():
    """Register"""
    return render_template("register.html")


@app.route('/process_registration')
def process_registration():
    """Check if the given username is in the database, and if not, add it"""
    pass

if __name__ == "__main__":
    # Set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
