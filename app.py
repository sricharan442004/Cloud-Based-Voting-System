from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)


API_CANDIDATES = "https://v824iep62c.execute-api.ap-south-1.amazonaws.com/candidates"
API_VOTE = "https://v824iep62c.execute-api.ap-south-1.amazonaws.com/vote"

@app.route("/")
def index():
   
    return render_template("index.html")

@app.route("/get_candidates")
def get_candidates():
    """Fetch candidates from API Gateway, sort by name, and return JSON data."""
    try:
        response = requests.get(API_CANDIDATES)
        response.raise_for_status()  
        candidates = sorted(response.json(), key=lambda c: c["name"])
        return jsonify(candidates)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/vote", methods=["POST"])
def vote():
    """Send a vote request to API Gateway."""
    try:
        data = request.json
        response = requests.post(API_VOTE, json=data)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
