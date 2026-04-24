# Philip Thompson 22024226
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from flask import Flask, request, jsonify
from predict_and_grade import run_pipeline, load_trained_model
import os

app = Flask(__name__)

model = load_trained_model()


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    try:
        result = run_pipeline(temp_path, model=model)
        return jsonify(result)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)