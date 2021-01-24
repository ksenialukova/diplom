from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import datetime

from backend.app.computing import run_analytics_for_params, get_plan_by_date
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
    if current_date > datetime.datetime.now().strftime("%Y-%m-%d"):
        df = db.return_forecast_intensities_and_coords_by_date(current_date)
    else:
        df = db.return_intensities_and_coords_by_date(current_date)
    df_branch = db.return_branch()
    cash_entities = []

    for index, row in df_branch.iterrows():
        cash_entities.append({
            'type': row['ce_type'],
            'lat': row['x_coord'],
            'lng': row['y_coord'],
            'intensity': 1
        })

    for index, row in df.iterrows():
        cash_entities.append({
            'type': row['ce_type'],
            'lat': row['x_coord'],
            'lng': row['y_coord'],
            'intensity': row['percent']
        })

    print(cash_entities)

    return jsonify({
        'cash_entities': cash_entities
    })


# получаем дату и выводим план на этот день, иначе пустой массив
@app.route('/plan_by_date')
def return_plan_by_date():
    date = request.args.get('date')
    print(get_plan_by_date(date))
    return jsonify({
        'plan': get_plan_by_date(date)
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
            'cost': row['cost'],
            'type': row['type'],
            'id': row['id']
        })

    return jsonify({
        'shipments': shipments
    })


@app.route('/run_analytics')
def run_analytics():
    date = request.args.get('date')
    # frequency = request.args.get('frequency')

    current_date = pd.to_datetime(date).strftime("%Y-%m-%d")

    try:
        run_analytics_for_params(current_date)
        return 'Success', 200
    except:
        print('error')
        return 'Error', 500


@app.route('/delete_shipment')
def delete_shipment():
    date = request.args.get('date')
    type = request.args.get('type')
    current_date = pd.to_datetime(date).strftime("%Y-%m-%d")
    try:
        status_code = db.delete_shipment(current_date, type)
        status_code = db.delete_forecast_balance(current_date)
        status_code = db.delete_forecast_entity_shipment(current_date)
        print(status_code)
        if status_code == 200:
            return 'Success', 200
        elif status_code == 500:
            return 'Error', 500
    except:
        return 'Error', 500


@app.route('/graph1')
def report_graph1():
    df = db.return_shipments()
    dates = df['date'].drop_duplicates()
    graph1 = []

    for date in dates:
        neighbour = int(df[(df['date'] == date) & (df['type'] == 'neighbour')]['cost'])
        bees = int(df[(df['date'] == date) & (df['type'] == 'bees')]['cost'])
        graph1.append({
            'date': pd.to_datetime(date).strftime("%Y-%m-%d"),
            'neighbour': neighbour,
            'bees': bees
        })
    print(graph1)

    return jsonify({
        'graph1': graph1
    })


@app.route('/graph2')
def report_graph2():
    df = db.return_shipments()
    dates = df['date'].drop_duplicates()
    graph2 = []

    for date in dates:
        neighbour = len(list(df[(df['date'] == date) & (df['type'] == 'neighbour')]['point'])[0])
        print(list(df[(df['date'] == date) & (df['type'] == 'neighbour')]['point'])[0])
        graph2.append({
            'date': pd.to_datetime(date).strftime("%Y-%m-%d"),
            'all': 9,
            'forecast': neighbour
        })
    print(graph2)

    return jsonify({
        'graph2': graph2
    })


@app.route('/upload')
def upload_file():
    print(request.args)

    return 'Success', 200


if __name__ == '__main__':
    np.random.seed(4)
    app.run(threaded=False, debug=True, host='0.0.0.0', port='5002')
