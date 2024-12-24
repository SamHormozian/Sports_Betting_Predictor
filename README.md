# NBA and NFL Game Outcome Predictor
## About the Sports Betting Predictor

Welcome to the **Sports Betting Predictor**, a personal project that combines data science, machine learning, and web development to predict the outcomes of sports games. This project is the result of my first attempt at implementing a neural network and serves as an exciting step into the world of machine learning and AI applications.

## What Does This Project Do?

The Sports Betting Predictor is designed to:
- **Ingest Data**: The project uses preloaded datasets in CSV format, along with web scrapers and API fetchers, to gather and update relevant sports data.
- **Data Preprocessing**: Includes cleaning, combining, and engineering features from the data to prepare it for model training. This step is crucial but introduced some challenges (described below).
- **Neural Network Training**: Implements a neural network with two hidden layers to predict outcomes, such as point spreads and total points in games.
- **Interactive User Interface**: A Flask-based application provides an intuitive interface where users can select a sport, teams, and game details, and receive predictions.

## Technology Stack

- **Data Sources**: Preloaded CSV files, Web Scrapers, and APIs
- **Data Preprocessing**: Python (Pandas, NumPy)
- **Machine Learning Model**: Neural Network with two hidden layers
- **Web Framework**: Flask
- **Frontend**: HTML, Bootstrap for user interaction

## Key Features

1. **Automated Data Pipeline**: Automates the process of gathering, preprocessing, and training the model.
2. **User-Friendly Interface**: A Flask-based application allows users to interact with the model seamlessly.
3. **Custom Neural Network**: Trains a basic two-hidden-layer neural network for sports prediction.

## Challenges and Limitations

This project is my first venture into creating and deploying a neural network, and as such, it comes with some limitations:

1. **Prediction Accuracy**: The accuracy of predictions is questionable, as this project is a learning experience, and further optimization is needed.
2. **Data Preprocessing Issues**: Challenges with team selection and usable features during preprocessing have occasionally affected the model's reliability.
3. **Feature Engineering**: Some features were one-hot encoded or dropped, limiting their interpretability and effectiveness for certain predictions.

## What I Learned

Through this project, I gained hands-on experience in:
- Building and training neural networks from scratch.
- Setting up a Flask application and creating a user-friendly interface.
- Working with real-world data pipelines, including data collection, cleaning, and feature engineering.

## Future Improvements

While the current version demonstrates the concept, there are several areas for future enhancement:
- **Model Optimization**: Improve the neural network architecture, tune hyperparameters, and explore advanced models for better accuracy.
- **Data Handling**: Address preprocessing challenges to include all teams and ensure cleaner feature selection.
- **Scalability**: Expand the app to include additional sports and datasets.

---

Thank you for visiting the Sports Betting Predictor! This project is not only a fun application but also a stepping stone in my journey into machine learning and AI. Feel free to explore, and I welcome any feedback or suggestions.

# Usage

### 1) Activate Virtual Environment (Optional)

- This project utilizes dependencies that need to be installed on your machine.
- If you do not want to install them, run ``` src/setup.py ``` and use ```venv/scripts/activate ``` to activate the virtual machine

### 2) Run Program

- The Program uses a master_pipeline to automate the entire process of running the application. These include installing dependencies, gathering updated data, combining and cleaning datasets, feature engineering, data splitting, nueral network training, and finally outputting the application on flask.
- To run this process, run ``` master_script.py```, then navigate to ```http://127.0.0.1:5000``` to interact with the application.
