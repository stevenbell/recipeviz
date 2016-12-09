from flask import Flask, jsonify, request
from search import search_recipes



app = Flask(__name__)
debug = False

@app.route("/")
def hello():
    return "You know nothing, John Snow."

# --------------------------------------------
# API
import json

@app.route('/search/<query>', methods=['GET'])
def search():
    with open('./assets/data/ingredients_simplified.json') as ingredients:
	return json.dumps(search_recipes(query, ingredients))
