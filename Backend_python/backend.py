from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from prediction import predict, predict_singlePlayer
import time
import numpy as np


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/predict_route', methods=['POST'])
def predict_route():

    app.logger.info('Received a prediction request.')
    data = request.get_json()
    app.logger.info('Received data: %s', data)


    player1 = data.get('player1')
    player2 = data.get('player2')
    model_type = data.get('model')

    if model_type == 'RandomForest (Recommended)':
        model_type = 'RandomForest'

    if player1 == player2:
        result_final = {
        'Accuracy': "Nice try :)",
        'Precision': "Select two different players to predict something",
        'Predictions': [1,1,1,1,1]

        }

        return jsonify(message="Select two different players :)"), 400

    if player2 == 'All (Default Single player mode)':
        result = predict_singlePlayer(player1, model_type)
    else:
        result = predict(player1, player2, model_type)

    # # Generate the URL for the image with a timestamp to prevent caching 
    image_url = url_for('static', filename='roc_curve.png') + '?t=' + str(int(time.time()))

    result['predictions'] = result['predictions'].tolist()

    result_final = {
        'Accuracy': result['Accuracy'],
        'Precision': result['Precision'],
        'Predictions': result['predictions'][0:5],
        'message': None
    }

    # Return the result and image URL as a dictionary
    response = {
        'result': result_final,
        'image_url': image_url
    }


    return jsonify(result_final)

if __name__ == '__main__':
    app.run(debug=True)



# chrome://net-internals/#sockets
