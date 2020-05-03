import datetime

from analytics.entity import Entity
from db.dbi import db

min_max_date = db.get_min_max_date()

start = min_max_date.loc[0, 'min']
end = min_max_date.loc[0, 'max']

date_range = [
    start + datetime.timedelta(days=x)
    for x in range(0, (end-start).days)
]

entities_df = db.get_atms()
entities = [Entity(i) for i in entities_df['ce_code']]

balances = db.get_balances()

for date in date_range:
    df = balances[balances['date'] == date]

    for entity in entities:
        percent_by_date = float(df[df['code'] == entity.code]['percent'])

        if entity.percent <= percent_by_date:
            entity.current_days += 1
        elif entity.percent > percent_by_date:
            entity.add_new_fulling(entity.current_days)
            entity.last_shipment_day = date
            entity.current_days = 1

        entity.percent = percent_by_date

window = 3
for entity in entities:
    mean_rolling = int(sum(entity.days_for_filling[-1-window:-1])/window)
    entity.days_to_next_shipment = mean_rolling
    entity.next_shipment_day = entity.last_shipment_day + datetime.timedelta(days=entity.days_to_next_shipment)

for entity in entities:
    db.add_forecast_shipment(ce_code=entity.code,
                             last_shipment=entity.last_shipment_day,
                             next_shipment=entity.next_shipment_day,
                             days_for_filling=entity.days_for_filling
                             )
