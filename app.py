from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from checker import evaluate_password, load_blocklist

app = Flask(__name__, static_folder="static")
CORS(app)  # allows the frontend to call this API from a different origin/port during development

blocklist = load_blocklist()


@app.route("/")
def serve_frontend():
    """Serve the frontend's index.html at the root URL."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/check-password", methods=["POST"])
def check_password():
    """
    Accepts JSON: {"password": "..."}
    Returns JSON: {"verdict": "...", "score": N, "errors": [...]}
    """
    data = request.get_json(silent=True)
    if not data or "password" not in data:
        return jsonify({"error": "Request body must include a 'password' field."}), 400

    password = data["password"]
    if not isinstance(password, str):
        return jsonify({"error": "'password' must be a string."}), 400

    result = evaluate_password(password, blocklist)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)