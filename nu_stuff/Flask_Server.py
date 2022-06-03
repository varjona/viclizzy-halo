# app.py
# curl http://127.0.0.1:5000/countries

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

def _find_next_id():
    return max(country["id"] for country in countries) + 1

@app.route('/')
def index():
    return json.dumps(countries)

@app.get("/countries")
def get_countries():
    return jsonify(countries)

@app.put("/countries")
def put_country():
    if request.is_json:
        country = json.loads(request.get_json())[0]
        for c in countries:
            if c["name"] == country["name"]:
               c["area"] = country["area"]
    return {"error": "Request must be JSON"}, 415


@app.post("/countries")
def add_country():
    if request.is_json:
        country = json.loads(request.get_json())[0]
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

if __name__ == '__main__':
    app.run(debug=True)
