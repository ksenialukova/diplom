import datetime

from db.dbi import db


def count_fulling_entities():
    min_max_date = db.get_min_max_date()

    start = min_max_date.loc[0, 'min']
    end = min_max_date.loc[0, 'max']

    date_range = [
        start + datetime.timedelta(days=x)
        for x in range(0, (end-start).days+1)
    ]

    entities_df = db.get_atms()
    entities_df['percent'] = 0
    entities_df['current_days'] = 0
    entities_df['intensity'] = 0

    balances = db.get_balances()

    for index, row in entities_df.iterrows():
        fulling_days = []
        for date in date_range:
            df = balances[balances['date'] == date]
            percent_by_date = float(df[df['code'] == row['ce_code']]['percent'])

            if entities_df.loc[index, 'percent'] <= percent_by_date:
                entities_df.loc[index, 'current_days'] += 1
            elif entities_df.loc[index, 'percent'] > percent_by_date:
                fulling_days.append(entities_df.loc[index, 'current_days'])
                entities_df.loc[index, 'current_days'] = 1

            entities_df.loc[index, 'percent'] = percent_by_date

        entities_df.loc[index, 'intensity'] = len(fulling_days)/sum(fulling_days)

    return entities_df

    """window = 3
    for entity in entities:
        mean_rolling = int(sum(entity.days_for_filling[-1-window:-1])/window)
        entity.days_to_next_shipment = mean_rolling
        entity.next_shipment_day = entity.last_shipment_day + datetime.timedelta(days=entity.days_to_next_shipment)

    for entity in entities:
        db.add_forecast_shipment(ce_code=entity.code,
                                 last_shipment=entity.last_shipment_day,
                                 next_shipment=entity.next_shipment_day,
                                 days_for_filling=entity.days_for_filling
                                 )"""
