import pandas as pd
from backend.app.salesmanpar import best_way
from backend.app.read_data import return_entities


def return_entities_for_next_shipment():
    return 2, 3, 4, 5, 6, 7, 8, 9


def return_plan():
    df_entities = return_entities()
    needed_entities = list(return_entities_for_next_shipment())

    table = (
        df_entities
        [lambda x: (x['CODE'].isin(needed_entities))]
    )

    X = list(
        df_entities
        [lambda x: (x['CODE'].isin(needed_entities))]['X_COORD']
    )

    Y = list(
        df_entities
        [lambda x: (x['CODE'].isin(needed_entities))]['Y_COORD']
    )

    print(table)

    plan = []

    S, ib, result_way = best_way(len(X), X, Y)
    print(result_way)

    for i in result_way:
        plan.append({
            'lat': table.loc[i+2, 'X_COORD'],
            'lng': table.loc[i+2, 'Y_COORD']
        })

    print(plan)
    return plan


return_plan()
