import random

from flask import Flask, json

app = Flask(__name__)

with open("all_data.json", "r") as f:
    j = json.load(f)


@app.route("/<path:path>")
def home(path):
    return json.jsonify(random.choices(j['restaurants'], k=10))
