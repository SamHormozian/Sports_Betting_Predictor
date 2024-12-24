import requests

# Define the API endpoint
API_URL = "http://127.0.0.1:5000/predict"

# Example test payload
# Replace the values with real or synthetic data for testing
payload = {
    "features": [
        2024,  # season
        1,     # regular (True -> 1)
        0,     # playoffs (False -> 0)
        0.2131147540983606,  # score_away
        0.146551724137931,  # score_home
        20, 15, 25, 20, 0,  # q1_away, q2_away, q3_away, q4_away, ot_away
        18, 19, 18, 21, 0,  # q1_home, q2_home, q3_home, q4_home, ot_home
        4.0,  # spread
        180.5,  # total
        155.0,  # moneyline_away
        -175.0,  # moneyline_home
        2.0,  # h2_spread
        89.0,  # h2_total
        0.0,  # id_spread
        0.0,  # id_total
        2.0612327703358573,  # price
        114.18986604542808,  # point
        0.4122137404580153,  # total_points
        0.3596664782362916,  # spread_accuracy
        3.5877862595419847,  # score_diff
        0,  # home_win (False -> 0)
        1,  # is_regular_season
        0,  # is_playoff
        1,  # commence_time_2024-12-25T22:00:00Z (one-hot encoded feature)
        0,  # commence_time_2024-12-25T17:00:00Z
        0,  # commence_time_2024-12-25T19:30:00Z
        0,  # additional one-hot encoded feature (if present)
        0,  # additional one-hot encoded feature (if present)
        0   # additional one-hot encoded feature (if present)
    ]
}


# Make a POST request to the API
response = requests.post(API_URL, json=payload)

# Check the response status
if response.status_code == 200:
    print("Prediction Successful!")
    print("Response:", response.json())
else:
    print(f"Error: Received status code {response.status_code}")
    print("Response:", response.text)
