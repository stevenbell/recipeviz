import os, copy
from flask import Flask, jsonify, request, send_from_directory, make_response

from search import search_recipes

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return app.make_response(open('assets/index.html').read())

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('assets/js', path)

# --------------------------------------------
# API
import json

@app.route('/search/<query>', methods=['GET'])
def search(query):
	return json.dumps(search_recipes(query, './assets/data/ingredients_simplified.json'))

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5050))
	app.run(host='0.0.0.0', port=port, debug=True)
