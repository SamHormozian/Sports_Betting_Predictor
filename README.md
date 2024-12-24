# NBA and NFL Game Outcome Predictor

## About the Sports Betting Predictor

Welcome to the **Sports Betting Predictor**, a personal project that combines data science, machine learning, and web development to predict the outcomes of sports games. This project represents my first attempt at implementing a neural network and is an exciting step into the world of machine learning and AI applications.

---

## What Does This Project Do?

The Sports Betting Predictor is designed to:
- **Ingest Data**: The project uses preloaded datasets in CSV format, along with web scrapers and API fetchers, to gather and update relevant sports data.
- **Data Preprocessing**: Cleans, combines, and engineers features from the data to prepare it for model training. This step is crucial but introduced some challenges (described below).
- **Neural Network Training**: Implements a neural network with two hidden layers to predict outcomes, such as point spreads and total points in games.
- **Interactive User Interface**: A Flask-based application provides an intuitive interface where users can select a sport, teams, and game details, and receive predictions.
- **Docker Integration**: Simplifies deployment and ensures environment consistency by containerizing the application.

---

## Technology Stack

- **Data Sources**: Preloaded CSV files, Web Scrapers, and APIs
- **Data Preprocessing**: Python (Pandas, NumPy)
- **Machine Learning Model**: Neural Network with two hidden layers
- **Web Framework**: Flask
- **Frontend**: HTML, Bootstrap for user interaction
- **Deployment**: Docker for containerized app delivery

---

## Key Features

1. **Automated Data Pipeline**: Automates the process of gathering, preprocessing, and training the model.
2. **User-Friendly Interface**: A Flask-based application allows users to interact with the model seamlessly.
3. **Custom Neural Network**: Trains a basic two-hidden-layer neural network for sports prediction.
4. **Dockerized Deployment**: Runs the entire application within a Docker container, eliminating dependency issues.

---

## Challenges and Limitations

This project is my first venture into creating and deploying a neural network, and as such, it comes with some limitations:

1. **Prediction Accuracy**: The accuracy of predictions is questionable, as this project is a learning experience, and further optimization is needed.
2. **Data Preprocessing Issues**: Challenges with team selection and usable features during preprocessing have occasionally affected the model's reliability.
3. **Feature Engineering**: Some features were one-hot encoded or dropped, limiting their interpretability and effectiveness for certain predictions.

---

## What I Learned

Through this project, I gained hands-on experience in:
- Building and training neural networks from scratch.
- Setting up a Flask application and creating a user-friendly interface.
- Working with real-world data pipelines, including data collection, cleaning, and feature engineering.
- Using Docker to containerize and deploy an application.

---

## Future Improvements

While the current version demonstrates the concept, there are several areas for future enhancement:
- **Model Optimization**: Improve the neural network architecture, tune hyperparameters, and explore advanced models for better accuracy.
- **Data Handling**: Address preprocessing challenges to include all teams and ensure cleaner feature selection.
- **Scalability**: Expand the app to include additional sports and datasets.
- **Improved Deployment**: Add continuous integration/continuous deployment (CI/CD) pipelines for streamlined updates.

---

## Usage

### 1) Activate Virtual Environment (Optional)
- This project utilizes dependencies that need to be installed on your machine.
- If you do not want to install them manually, run `src/setup.py` and use `venv/scripts/activate` to activate the virtual environment.

---

### 2) Run the Program

#### Without Docker:
1. Use the **master pipeline script** (`master_script.py`) to automate:
    - Installing dependencies
    - Gathering updated data
    - Combining and cleaning datasets
    - Feature engineering
    - Data splitting
    - Neural network training
    - Flask app deployment
2. Once the pipeline completes, navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to interact with the app.

---

#### With Docker:
1. Ensure [Docker is installed](https://docs.docker.com/get-docker/) on your system.
2. Build the Docker image:
   ```bash
   docker build -t sports-betting-predictor .
### 3) Stopping the Application

#### Flask Development Server:
If using the Flask development server, press `CTRL+C` in the terminal running the app.

#### Docker:
- To stop the Docker container:
  ```bash
  docker stop sports-betting-app

#### To remove the Docker container:
```bash
docker rm sports-betting-app

Thank you for exploring the Sports Betting Predictor! Feel free to reach out for feedback or suggestions. Happy predicting!