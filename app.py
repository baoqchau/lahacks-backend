from flask import Flask, jsonify, abort, make_response, request
import pyrebase
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

predictions = [
    {
        'id':'1',
        'sports': u'Soccer',
        'votes':{
	   'USA': 500,
	   'Russia': 1000,
           'China': 200,
	   'India': 150
        },
        'country': {
            'name': 'USA',
            'number': 50
        }
    },
    {
        'sports': u'Swimming',
        'votes':{
            'USA':1200,
            'Russia':420,
            'India':500,
            'China':250
        },
        'id':'2',
        'country': {
            'name': 'China',
            'number': 40
        }
    },
    {
        'sports': u'Skiing',
        'votes':{
            'Russia':430,
            'USA':240,
            'German':450,
            'China': 460
        },
        'id':'3',
        'country': {
            'name': 'Russia',
            'number': 60 
        }
    },
    {
        'sports': u'Basketball',
        'votes': {
            'China': 430,
            'USA': 340,
            'Russia': 550,
            'India': 660
        },
        'id': '4',
        'country': {
            'name': 'Canada',
            'number': 50
        }
    },
    {
        'sports': u'Ping-pong',
        'votes': {
            'China': 750,
            'India': 840,
            'Russia': 660,
            'USA': 1070
        },
        'id': '5',
        'country': {
            'name': 'France',
            'number': 80
        }
    },
    {
        'sports': u'Bowling',
        'votes': {
            'India': 850,
            'USA': 460,
            'China': 540,
            'Russia': 1060
        },
        'id': '6',
        'country':{
            'name': 'German',
            'number': 40
        }
    },
    {
        'sports': u'Volleyball',
        'votes': {
            'India': 760,
            'USA': 850,
            'Russia': 1040,
            'China': 970
        },
        'id': '7',
        'country': {
            'name': 'Mexico',
            'number': 70
        }
    },
    {
        'sports': u'Badminton',
        'votes': {
            'China': 660,
            'USA': 750,
            'Russia': 240,
            'India': 970
        },
        'id': '8',
        'country': {
            'name': 'Spain',
            'number': 70
        }
    },
    {
        'sports': u'Badminton',
        'votes': {
            'Russia': 1060,
            'USA': 950,
            'China': 840,
            'India': 870
        },
        'id': '9',
        'country': {
            'name': 'India',
            'number': 70
        }
    },
    {
        'sports': u'Badminton',
        'votes': {
            'USA': 980,
            'India': 1050,
            'Russia': 440,
            'China': 870
        },
        'id': '10',
        'country': {
            'name': 'Japan',
            'number': 70
        }
    }
]

#firebase config
config = { 
        'apiKey': 'AIzaSyAVYaVejXdtzx_jOuXT_ZY_oK6_w408KQ8',
        'authDomain': 'goalcoach-fe998.firebaseapp.com',
        'databaseURL': 'https://goalcoach-fe998.firebaseio.com',
        'projectId': 'goalcoach-fe998',
        'storageBucket': 'goalcoach-fe998.appspot.com',
        'messagingSenderId': '945732490440'
    }


#firebase setup
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
#authenticate a user
user = auth.sign_in_with_email_and_password("baoqchau@gmail.com", "hocgioi1")
user = auth.refresh(user['refreshToken'])

db = firebase.database()
#db.child("predictions").set(predictions, user['idToken'])


@app.route('/fantasy/api/v1.0/predictions', methods=['GET', 'OPTIONS'])
def get_predictions():
    results = db.child("predictions").get(user['idToken'])
    data =[] 
    for prediction in results.each():
        data.append(prediction.val())
    return jsonify({'predictions': data})

@app.route('/fantasy/api/v1.0/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    number = str(prediction_id)
    data = get_predictions()
    prediction = []
    for ele in data:
        if ele["id"] == number:
            prediction.append(ele)
    print(prediction)
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
    idNeed = str(prediction_id-1)
    prediction = [prediction for prediction in predictions if prediction['id'] == prediction_id]
 #   if len(prediction) == 0:
 #       abort(404)
 #   if not request.json:
 #       abort(400)
    country = request.json.get("vote")
    votes =db.child("predictions").child(idNeed).child("votes").child(country).get(user['idToken']).val()
    votes = votes + 10
    db.child("predictions").child(idNeed).child("votes").update({country:votes},user['idToken'])
    print('update successful')
    return 'update successful' 

@app.route('/')
def hello_world():
    return 'Hello, World!'
