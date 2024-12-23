import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Define directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SPLITS_DIR = os.path.join(PROJECT_ROOT, "data", "splits")
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
PLOTS_DIR = os.path.join(PROJECT_ROOT, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)  # Create plots directory if it doesn't exist

# Activation function
def sigmoid(x):
    try:
        return 1 / (1 + np.exp(-x))
    except Exception as e:
        print(f"Error in sigmoid function: {e}")
        print(f"Input type: {type(x)}, input value: {x}")
        raise

# Forward pass
def forward_propagation(X, weights):
    print("Debug: Forward propagation started")
    print(f"Input X type: {type(X)}, dtype: {getattr(X, 'dtype', 'N/A')}, shape: {getattr(X, 'shape', 'N/A')}")
    print(f"Weights w1 shape: {weights['w1'].shape}, dtype: {weights['w1'].dtype}")
    
    X = np.array(X, dtype=np.float64)

    z1 = np.dot(X, weights["w1"]) + weights["b1"]
    z1 = np.array(z1, dtype=np.float64)
    a1 = sigmoid(z1)
    print(f"Layer 1: z1 shape: {z1.shape}, a1 shape: {a1.shape}")

    z2 = np.dot(a1, weights["w2"]) + weights["b2"]
    z2 = np.array(z2, dtype=np.float64)
    a2 = sigmoid(z2)
    print(f"Layer 2: z2 shape: {z2.shape}, a2 shape: {a2.shape}")

    z3 = np.dot(a2, weights["w3"]) + weights["b3"]
    z3 = np.array(z3, dtype=np.float64)
    a3 = z3
    print(f"Output layer: z3 shape: {z3.shape}, a3 shape: {a3.shape}")

    return a3

# Load dataset
def load_data(file_name):
    file_path = os.path.join(SPLITS_DIR, file_name)
    data = pd.read_csv(file_path)
    
    print(f"Loading data from {file_name}...")
    print("Dataset sample:")
    print(data.head())
    print("Dataset column types:")
    print(data.dtypes)
    
    drop_cols = ["date", "score_diff_bin", "away", "home", "whos_favored", 
                 "home_team_combined", "away_team_combined", "home_team", 
                 "away_team", "bookmaker", "market_type", "name"]
    data = data.drop(columns=drop_cols)
    data = pd.get_dummies(data, drop_first=True)
    
    X = data.drop(columns=["score_diff"]).values
    y = data["score_diff"].values.reshape(-1, 1)
    
    print("Transformed Dataset sample (after encoding and dropping):")
    print(data.head())
    print("Transformed Dataset column types:")
    print(data.dtypes)
    
    return X, y

# Load model weights
def load_model():
    model_path = os.path.join(MODEL_DIR, "nn_weights.npy")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model weights file not found at {model_path}")
    weights = np.load(model_path, allow_pickle=True).item()
    print(f"Model loaded from {model_path}")
    return weights

# Evaluate the model
def evaluate_model():
    print("Loading test data...")
    X_test, y_test = load_data("nba_test.csv")

    print("Loading saved model weights...")
    weights = load_model()

    print("Performing forward propagation...")
    y_pred = forward_propagation(X_test, weights)

    print("Calculating Mean Squared Error...")
    mse = np.mean((y_pred - y_test) ** 2)
    print(f"Mean Squared Error on Test Data: {mse:.4f}")

    # Residual Plot
    print("Plotting residuals...")
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, residuals, alpha=0.6, edgecolor="k")
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title("Residual Plot")
    plt.xlabel("Actual Values (y_test)")
    plt.ylabel("Residuals (y_test - y_pred)")
    plt.grid(True)
    
    residual_plot_path = os.path.join(PLOTS_DIR, "residual_plot.png")
    plt.savefig(residual_plot_path, dpi=300)
    print(f"Residual plot saved at {residual_plot_path}")

    # Histogram of Residuals
    print("Plotting histogram of residuals...")
    plt.figure(figsize=(10, 6))
    plt.hist(residuals, bins=30, edgecolor="k", alpha=0.7)
    plt.title("Histogram of Residuals")
    plt.xlabel("Residuals (y_test - y_pred)")
    plt.ylabel("Frequency")
    plt.grid(True)
    
    histogram_path = os.path.join(PLOTS_DIR, "residual_histogram.png")
    plt.savefig(histogram_path, dpi=300)
    print(f"Histogram of residuals saved at {histogram_path}")

if __name__ == "__main__":
    evaluate_model()
