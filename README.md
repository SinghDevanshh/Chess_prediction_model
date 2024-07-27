# Chess Prediction Model

This project is a web application that predicts the outcomes of chess games using historical data from chess.com archives. The application consists of a Flask API backend and a React frontend, integrating four different predictive models to analyze and predict the outcomes for eight chess players.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Hosted Application](#hosted-application)
- [Contributing](#contributing)

## Features

- Predicts outcomes of chess games for eight players.
- Integrates four different predictive models.
- User-friendly React frontend for interaction.
- Flask API backend for handling predictions.

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/singhdevanshh/chess-prediction-model.git
    cd chess-prediction-model/backend
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:

    ```bash
    flask run
    ```

### Frontend Setup

1. Navigate to the frontend directory:

    ```bash
    cd ../frontend
    ```

2. Install the required dependencies:

    ```bash
    npm install
    ```

3. Start the React app:

    ```bash
    npm start
    ```

## Usage

1. Ensure both the backend and frontend servers are running.
2. Open your browser and navigate to `http://localhost:3000`.
3. Interact with the application to predict chess game outcomes.

## Technologies

- **Backend:**
  - Python
  - Flask
- **Frontend:**
  - React
  - Tailwind CSS
- **Machine Learning:**
  - scikit-learn
  - pandas
  - numpy

## Project Structure

```plaintext
chess-prediction-model/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── ... (other backend files)
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ... (other frontend files)
│
└── README.md
```

## Hosted Application

- The Chess Prediction Model application is hosted on Render. You can access it at the following URL:
- https://chess-prediction-model-frontend.onrender.com/
- Feel free to visit and interact with the application to see the predictions in action. 
- When using the application, it may appear that nothing happens when you click the submit button. This is due to the Render server rebooting after a period of inactivity. Please wait for a few minutes, then refresh the page. The website should then work seamlessly.

## Contributing

- Contributions are welcome! Please open an issue or submit a pull request for any changes.