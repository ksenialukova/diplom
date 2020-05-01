from flask import Flask
from flask import jsonify
from flask_cors import CORS
import numpy as np

from backend.app.computing import return_plan

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


# получаем дату и возвращаем текущие интенсивности
@app.route('/intensity')
def return_intensity():
    return jsonify({
        'cash_entities': [
            {
                'type': 'atm',
                'lat': 50.4246741,
                'lng': 30.4601089,
                'intensity': 0.5
            },
            {
                'type': 'atm',
                'lat': 50.4338805,
                'lng': 30.4532582,
                'intensity': 0.75
            }
        ]
    })


# получаем дату и выводим план на этот день, иначе пустой массив
@app.route('/plan_by_date')
def return_plan_by_date():
    return jsonify({
        'plan': return_plan()
    })


# вывод списка с бд
@app.route('/shipments')
def get_shipments():
    return jsonify({
        'shipments': [
            {
                'date': '2020-04-23',
                'length': '250',
                'cost': '1000'
            },
            {
                'date': '2020-04-01',
                'length': '350',
                'cost': '1000'
            },
            {
                'date': '2020-03-23',
                'length': '450',
                'cost': '1000'
            },
            {
                'date': '2020-03-01',
                'length': '250',
                'cost': '900'
            },
            {
                'date': '2020-02-23',
                'length': '450',
                'cost': '1000'
            }
        ]
    })


if __name__ == '__main__':
    np.random.seed(4)
    app.run(threaded=False, debug=True, host='0.0.0.0', port='5002')
