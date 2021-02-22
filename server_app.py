import os

from contentgenerator import wikiscraper
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/get', methods=['GET'])
def respond():
    """Send Get response"""
    primary_keyword = request.args.get("pri").replace("_", " ")
    secondary_keyword = request.args.get("sec").replace("_", " ")

    # Handles error of primary and secondary keywords not included
    if not primary_keyword or not secondary_keyword:
        return "Error keyword missing"
    response = {"primary_keyword": primary_keyword,
                "secondary_keyword": secondary_keyword}

    search = [[primary_keyword, secondary_keyword]]
    paragraph = wikiscraper(search)

    response["wiki"] = paragraph[0][2]
    return jsonify(response)


@app.route('/')
def index():
    return "Enter a get in the following format. /get?pri=puppy&sec=dog"


if __name__ == "__main__":
    # Start App, Use environment port or port 5001
    app.run(port=(os.getenv('PORT') if os.getenv('PORT') else 5001))
