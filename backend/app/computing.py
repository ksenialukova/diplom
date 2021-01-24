import pandas as pd
import datetime
from backend.app.salesmanpar import best_way
from backend.app.beealgo import bees_algo
from analytics.count_fulling_entities import count_fulling_entities
from db.dbi import db


def return_entities_for_shipment_by_date(date):
    df = list(db.get_entities_for_shipment_by_date(date)['ce_code'])
    return df


def return_plan(date):
    depo = 1
    df_entities = db.get_entities(depo=1)
    df_costs = db.get_costs()
    needed_entities = return_entities_for_shipment_by_date(date)

    X = list(
        df_entities
        [lambda x: (x['ce_code'].isin(needed_entities))]['ce_code']
    )

    X.append(depo)

    M = {}
    for i in X:
        temp = {}
        for j in X:
            if i == j:
                temp[j] = float('inf')
            else:
                temp[j] = int(df_costs[
                                  (df_costs['from_code'] == i)
                                  &
                                  (df_costs['to_code'] == j)
                                  ]['duration']
                              )
        M[i] = temp

    legths = {}
    for i in X:
        temp = {}
        for j in X:
            if i == j:
                temp[j] = float('inf')
            else:
                temp[j] = int(df_costs[
                                  (df_costs['from_code'] == i)
                                  &
                                  (df_costs['to_code'] == j)
                                  ]['distance']
                              )
        legths[i] = temp

    S, ib, result_way = best_way(M, X, depo)

    length = 0
    for i in range(len(result_way) - 1):
        length += legths[result_way[i]][result_way[i + 1]]

    return S, ib, result_way, length


def return_plan_bees(date):
    depo = 1
    df_entities = db.get_entities(depo=1)
    df_costs = db.get_costs()
    needed_entities = return_entities_for_shipment_by_date(date)

    X = list(
        df_entities
        [lambda x: (x['ce_code'].isin(needed_entities))]['ce_code']
    )

    X.append(depo)

    M = {}
    for i in X:
        temp = {}
        for j in X:
            if i == j:
                temp[j] = float('inf')
            else:
                temp[j] = int(df_costs[
                                  (df_costs['from_code'] == i)
                                  &
                                  (df_costs['to_code'] == j)
                                  ]['duration']
                              )
        M[i] = temp

    legths = {}
    for i in X:
        temp = {}
        for j in X:
            if i == j:
                temp[j] = float('inf')
            else:
                temp[j] = int(df_costs[
                                  (df_costs['from_code'] == i)
                                  &
                                  (df_costs['to_code'] == j)
                                  ]['distance']
                              )
        legths[i] = temp

    S, result_way = bees_algo(M, X, depo)

    length = 0
    for i in range(len(result_way) - 1):
        length += legths[result_way[i]][result_way[i + 1]]

    return S, result_way, length


def get_plan_by_date(date):
    result_way = (
        db.get_plan_by_date(date).loc[0, 'point']
        if len(db.get_plan_by_date(date))
        else []
    )

    df_coords = db.get_coords()
    plan = []
    for i in result_way:
        plan.append({
            'lat': float(df_coords[df_coords['ce_code'] == i]['x_coord']),
            'lng': float(df_coords[df_coords['ce_code'] == i]['y_coord'])
        })

    return plan


def run_analytics_for_params(date):

    df = db.get_balances_by_date(date)
    entities = count_fulling_entities()
    print(df, entities)

    for i in range(2):
        for index, row in entities.iterrows():
            db.fill_balance(
                code=int(row['ce_code']),
                date=(pd.to_datetime(date)+datetime.timedelta(days=i+1)),
                percent=(row['percent']+row['intensity']*(i+1))
            )

    for index, row in entities.iterrows():
        reco_today = row['percent'] + row['intensity']
        reco_tomorrow = row['percent'] + row['intensity'] * 2

        if reco_today > 1:
            db.add_forecast_shipment(
                ce_code=row['ce_code'],
                next_shipment=(pd.to_datetime(date)+datetime.timedelta(days=1))
            )
        elif (reco_today < 1) and (reco_tomorrow > 1):
            if abs(reco_today - 1) > (reco_tomorrow - 1):
                db.add_forecast_shipment(
                    ce_code=row['ce_code'],
                    next_shipment=(pd.to_datetime(date) + datetime.timedelta(days=2))
                )
            else:
                db.add_forecast_shipment(
                    ce_code=row['ce_code'],
                    next_shipment=(pd.to_datetime(date) + datetime.timedelta(days=1))
                )

    for date in [pd.to_datetime(date) + datetime.timedelta(days=1),
                 pd.to_datetime(date) + datetime.timedelta(days=2)]:
        S, ib, result_way, length = return_plan(date)
        if S != float('inf'):
            db.add_plan(date, result_way, length, S, 'neighbour')

        S, result_way, length = return_plan_bees(date)
        if S != float('inf'):
            db.add_plan(date, result_way, length, S, 'bees')
