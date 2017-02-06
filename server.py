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

    return "This is Amanda's recipeapp homepage"

if __name__ == "__main__":
    # Set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
