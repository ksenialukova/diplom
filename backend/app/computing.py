import pandas as pd
from backend.app.salesmanpar import best_way
from backend.app.read_data import return_entities
from db.dbi import db


def return_entities_for_next_shipment():
    return 2, 3, 4


def return_plan():
    depo = 1
    df_entities = db.get_entities(depo=1)
    df_costs = db.get_costs()
    needed_entities = list(return_entities_for_next_shipment())

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
                                  ]['distance']
                              )
        M[i] = temp

    S, ib, result_way = best_way(M, X, depo)
    print(result_way)

    # print(plan)
    # return plan


return_plan()
