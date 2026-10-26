from flask import Flask, request, jsonify
from datetime import datetime, timezone
import os

app = Flask(__name__)

latest_data = {
    "temperature": None,
    "humidity": None,
    "shock_g": None,
    "tilt": None,
    "latitude": None,
    "longitude": None,
    "gps_valid": False,
    "updated_at": None
}

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/")
def home():
    return jsonify({
        "message": "Organ Transportation backend is running"
    })

@app.route("/api/data", methods=["GET", "OPTIONS"])
def get_data():
    if request.method == "OPTIONS":
        return "", 204
    return jsonify(latest_data)

@app.route("/api/data", methods=["POST", "OPTIONS"])
def receive_data():
    if request.method == "OPTIONS":
        return "", 204

    incoming = request.get_json(silent=True)

    if not isinstance(incoming, dict):
        return jsonify({"error": "Send JSON data"}), 400

    allowed_keys = [
        "temperature", "humidity", "shock_g", "tilt",
        "latitude", "longitude", "gps_valid"
    ]

    for key in allowed_keys:
        if key in incoming:
            latest_data[key] = incoming[key]

    latest_data["updated_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    print("Received sensor data:", latest_data)
    return jsonify({"success": True}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
