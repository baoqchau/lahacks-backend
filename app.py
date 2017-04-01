from flask import Flask, jsonify, abort, make_response, request
app = Flask(__name__)

predictions = [
    {
        'id':1,
        'sports': u'Soccer',
        'votes':{
            'Canada': 0,
            'Mexico': 0,
            'France': 0,
            'China': 0
        }
    },
    {
        'sports': u'Swimming',
        'votes':{
            'Canada':0,
            'USA':0,
            'India':0,
            'China':0
        },
        'id':2
    },
    {
        'sports': u'Skiing',
        'votes':{
            'Canada':0,
            'USA':0,
            'German':0,
            'India':0
        },
        'id':3
    }
]

#firebase config
config = [
    { 
        'apiKey': 'AIzaSyAVYaVejXdtzx_jOuXT_ZY_oK6_w408KQ8',
        'authDomain': 'goalcoach-fe998.firebaseapp.com',
        'databaseURL': 'https://goalcoach-fe998.firebaseio.com',
        'projectId': 'goalcoach-fe998',
        'storageBucket': 'goalcoach-fe998.appspot.com',
        'messagingSenderId': '945732490440'
    }
]

@app.route('/fantasy/api/v1.0/predictions', methods=['GET'])
def get_tasks():
    return jsonify({'predictions': predictions})

@app.route('/fantasy/api/v1.0/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    prediction = [prediction for prediction in predictions if prediction['id'] == prediction_id]
    if len(prediction) == 0:
        abort(404)
    return jsonify({'prediction': prediction[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/fantasy/api/v1.0/predictions', methods=['POST'])
def create_task():
    if not request.json or not 'sports' in request.json:
        abort(400)
    prediction = {
        'id': prediction[-1]['id'] + 1,
        'sports': request.json['sports'],
        'votes': request.json.get('votes', ""),
    }
    predictions.append(prediction)
    return jsonify({'prediction': prediction}), 201

@app.route('/fantasy/api/v1.0/predictions/<int:prediction_id>', methods=['PUT'])
def update_prediction(prediction_id):
    prediction = [prediction for prediction in predictions if prediction['id'] == prediction_id]
    if len(prediction) == 0:
        abort(404)
    if not request.json:
        abort(400)
    country = request.json.get("vote")
    for choice in prediction[0]['votes']:
        if choice == country:
            prediction[0]['votes'][choice] += 1
    print(country)
    return jsonify({'prediction': prediction[0]})

@app.route('/')
def hello_world():
        return 'Hello, World!'
