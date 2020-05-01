import datetime
import pandas as pd

from analytics.entity import Entity

start_date = '2020-03-01'
end_date = '2020-03-31'

start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

date_range = [
    start + datetime.timedelta(days=x)
    for x in range(0, (end-start).days)
]

entity_number = 10
entities = [Entity(f'A{i}') for i in range(entity_number)]

for date in date_range:
    df = pd.read_csv(f'../data/balances/balances.{date}.csv', index_col=1)
    for entity in entities:

        if entity.percent <= df.loc[entity.code]['PERCENT']:
            entity.current_days += 1
        elif entity.percent > df.loc[entity.code]['PERCENT']:
            entity.add_new_fulling(entity.current_days)
            entity.current_days = 1

        entity.percent = df.loc[entity.code]['PERCENT']

for entity in entities:
    print(entity.code, entity.days_for_fulling, entity.percent)
