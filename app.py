from flask import Flask, render_template, request, jsonify
import numpy as np
import os

# Define directories
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "models"))

# Load model weights
def load_model():
    model_path = os.path.join(MODEL_DIR, "nn_weights.npy")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model weights file not found at {model_path}")
    weights = np.load(model_path, allow_pickle=True).item()
    return weights

# Activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Forward pass
def forward_propagation(X, weights):
    X = np.array(X, dtype=np.float64)
    z1 = np.dot(X, weights["w1"]) + weights["b1"]
    a1 = sigmoid(z1)
    z2 = np.dot(a1, weights["w2"]) + weights["b2"]
    a2 = sigmoid(z2)
    z3 = np.dot(a2, weights["w3"]) + weights["b3"]
    a3 = z3  # Output layer (no activation for regression)
    return a3

# Flask app
app = Flask(__name__)

# Load the model weights once when the app starts
weights = load_model()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        required_fields = ["sport", "homeTeam", "awayTeam", "spread", "totalPoints"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Map user inputs to the 37 feature vector
        features = []
        features.append(1 if data["sport"] == "nba" else 0)  # Example: sport encoding
        features.extend([
            data["spread"],
            data["totalPoints"],
        ])

        # Add dummy values for one-hot encodings or placeholders
        # Ensure the features array has 37 elements
        features += [0] * (37 - len(features))

        # Reshape for prediction
        features = np.array(features).reshape(1, -1)
        prediction = forward_propagation(features, weights)

        return jsonify({"prediction": float(prediction[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
