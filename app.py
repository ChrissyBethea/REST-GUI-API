
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route("/purchase", methods=["POST"])
def create_purchase():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    required = ["product_id", "description", "name", "email", "price", "online"]
    if any(field not in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    email = str(data["email"])
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({"error": "Invalid email address"}), 400

    try:
        price = float(data["price"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price"}), 400

    if not 0 <= price <= 1000:
        return jsonify({"error": "Price must be between $0 and $1,000"}), 400

    if not isinstance(data["online"], bool):
        return jsonify({"error": "Invalid purchase status"}), 400

    return jsonify({
        "message": "Purchase submitted successfully!",
        "purchase": data
    }), 201


if __name__ == "__main__":
    app.run(port=5001, debug=True)
