from flask import Flask, request, jsonify
import json

app = Flask(__name__)

data = [
    {"id": 1, "position": (0, 0), "color": "RED"}
]

def _find_next_id():
    return max(item["id"] for item in data) + 1

@app.route('/')
def index():
    return json.dumps(data)

@app.get("/data")
def get_data():
    return jsonify(data)

# Put overwrites data
@app.put("/data")
def put_positions():
    if request.is_json:
        put_data = json.loads(request.get_json())[0]
        for item in data:
            if item["id"] == put_data["id"]:
                item["position"] = put_data["position"]
                item["color"] = put_data["color"]
        return put_data, 200
    return {"error": "Request must be JSON"}, 415

# Post adds data
@app.post("/data")
def add_data():
    if request.is_json:
        post_data = json.loads(request.get_json())[0]
        post_data["id"] = _find_next_id()
        data.append(post_data)
        return post_data, 201
    return {"error": "Request must be JSON"}, 415

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)