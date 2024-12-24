import numpy as np
import pandas as pd
import os

# Define directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SPLITS_DIR = os.path.join(PROJECT_ROOT, "data", "splits")
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Hyperparameters
INPUT_SIZE = 43  # Adjust this based on your dataset's features
HIDDEN_SIZE_1 = 64
HIDDEN_SIZE_2 = 32
OUTPUT_SIZE = 1  # For regression (e.g., score_diff), set to 1
LEARNING_RATE = 0.01
EPOCHS = 100

# Initialize weights and biases
def initialize_weights(input_size, hidden_size_1, hidden_size_2, output_size):
    np.random.seed(42)
    weights = {
        "w1": np.random.randn(input_size, hidden_size_1).astype(np.float64) * 0.01,
        "b1": np.zeros((1, hidden_size_1), dtype=np.float64),
        "w2": np.random.randn(hidden_size_1, hidden_size_2).astype(np.float64) * 0.01,
        "b2": np.zeros((1, hidden_size_2), dtype=np.float64),
        "w3": np.random.randn(hidden_size_2, output_size).astype(np.float64) * 0.01,
        "b3": np.zeros((1, output_size), dtype=np.float64),
    }
    return weights

# Activation function
def sigmoid(x):
    x = np.array(x, dtype=np.float64)  # Ensure x is a NumPy array with float64 dtype
    x_clipped = np.clip(x, -500, 500)  # Clip values to prevent overflow in np.exp
    return 1 / (1 + np.exp(-x_clipped))

def sigmoid_derivative(x):
    return x * (1 - x)

# Forward pass
def forward_propagation(X, weights):
    X = np.array(X, dtype=np.float64)  # Ensure X is a NumPy array of floats
    z1 = np.dot(X, weights["w1"]) + weights["b1"]
    print(f"Debug: z1 type={type(z1)}, dtype={z1.dtype}, shape={z1.shape}")
    a1 = sigmoid(z1)
    z2 = np.dot(a1, weights["w2"]) + weights["b2"]
    print(f"Debug: z2 type={type(z2)}, dtype={z2.dtype}, shape={z2.shape}")
    a2 = sigmoid(z2)
    z3 = np.dot(a2, weights["w3"]) + weights["b3"]
    print(f"Debug: z3 type={type(z3)}, dtype={z3.dtype}, shape={z3.shape}")
    a3 = z3  # Output layer (no activation for regression)
    cache = {"z1": z1, "a1": a1, "z2": z2, "a2": a2, "z3": z3, "a3": a3}
    return a3, cache

# Backward pass
def backward_propagation(X, y, weights, cache):
    X = np.array(X, dtype=np.float64)  # Ensure X is float64
    y = np.array(y, dtype=np.float64)  # Ensure y is float64
    m = X.shape[0]

    dz3 = cache["a3"] - y
    dw3 = np.dot(cache["a2"].T, dz3) / m
    db3 = np.sum(dz3, axis=0, keepdims=True) / m

    dz2 = np.dot(dz3, weights["w3"].T) * sigmoid_derivative(cache["a2"])
    dw2 = np.dot(cache["a1"].T, dz2) / m
    db2 = np.sum(dz2, axis=0, keepdims=True) / m

    dz1 = np.dot(dz2, weights["w2"].T) * sigmoid_derivative(cache["a1"])
    dw1 = np.dot(X.T, dz1) / m
    db1 = np.sum(dz1, axis=0, keepdims=True) / m

    gradients = {
        "dw1": np.array(dw1, dtype=np.float64),
        "db1": np.array(db1, dtype=np.float64),
        "dw2": np.array(dw2, dtype=np.float64),
        "db2": np.array(db2, dtype=np.float64),
        "dw3": np.array(dw3, dtype=np.float64),
        "db3": np.array(db3, dtype=np.float64),
    }

    return gradients

# Update weights
def update_weights(weights, gradients, learning_rate):
    for key in weights.keys():
        weights[key] -= learning_rate * gradients["d" + key]
    return weights

# Mean Squared Error
def compute_loss(y_pred, y):
    return np.mean((y_pred - y) ** 2)

# Load dataset
def load_data(file_name):
    file_path = os.path.join(SPLITS_DIR, file_name)
    data = pd.read_csv(file_path)
    print(f"Loading data from {file_name}...")
    drop_cols = ["date", "score_diff_bin", "away", "home", "whos_favored", 
                 "home_team_combined", "away_team_combined", "home_team", 
                 "away_team", "bookmaker", "market_type", "name"]
    data = data.drop(columns=drop_cols)
    data = pd.get_dummies(data, drop_first=True)
    X = data.drop(columns=["score_diff"]).values
    y = data["score_diff"].values.reshape(-1, 1)
    return X, y

# Training the model
def train_neural_network():
    print("Loading training data...")
    X_train, y_train = load_data("nba_train.csv")
    X_val, y_val = load_data("nba_val.csv")
    global INPUT_SIZE
    INPUT_SIZE = X_train.shape[1]
    print(f"Detected INPUT_SIZE: {INPUT_SIZE}")
    print("Initializing weights...")
    weights = initialize_weights(INPUT_SIZE, HIDDEN_SIZE_1, HIDDEN_SIZE_2, OUTPUT_SIZE)
    for epoch in range(EPOCHS):
        y_pred, cache = forward_propagation(X_train, weights)
        train_loss = compute_loss(y_pred, y_train)
        gradients = backward_propagation(X_train, y_train, weights, cache)
        weights = update_weights(weights, gradients, LEARNING_RATE)
        y_val_pred, _ = forward_propagation(X_val, weights)
        val_loss = compute_loss(y_val_pred, y_val)
        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{EPOCHS} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
    save_model(weights)

# Save model weights
def save_model(weights):
    model_path = os.path.join(MODEL_DIR, "nn_weights.npy")
    np.save(model_path, weights)
    print(f"Model saved at {model_path}")

if __name__ == "__main__":
    train_neural_network()
