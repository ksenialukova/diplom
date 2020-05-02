from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sqlalchemy import create_engine
import pandas as pd

from backend.app.computing import return_plan
from db.dbi import DiplomDB, get_db_connection_str

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

engine = create_engine(get_db_connection_str())

db = DiplomDB(engine)


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


# получаем дату и возвращаем текущие интенсивности
@app.route('/intensity')
def return_intensity():
    date = request.args.get('date')
    current_date = pd.to_datetime(date).strftime("%Y-%m-%d")
    df = db.return_intensities_and_coords_by_date(current_date)
    cash_entities = []

    for index, row in df.iterrows():
        cash_entities.append({
            'type': row['ce_type'],
            'lat': row['x_coord'],
            'lng': row['y_coord'],
            'intensity': row['percent']
        })

    return jsonify({
        'cash_entities': cash_entities
    })


# получаем дату и выводим план на этот день, иначе пустой массив
@app.route('/plan_by_date')
def return_plan_by_date():
    date = request.args.get('date')
    return jsonify({
        'plan': return_plan()
    })


# вывод списка с бд
@app.route('/shipments')
def get_shipments():
    df = db.return_shipments()
    shipments = []

    for index, row in df.iterrows():
        shipments.append({
            'date': row['date'].strftime("%Y-%m-%d"),
            'length': row['length'],
            'cost': row['cost']
        })

    return jsonify({
        'shipments': shipments
    })


if __name__ == '__main__':
    np.random.seed(4)
    app.run(threaded=False, debug=True, host='0.0.0.0', port='5002')
