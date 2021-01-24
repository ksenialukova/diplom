import datetime
import csv
import random

from db.dbi import db

start_date = '2020-01-01'
end_date = '2020-06-16'

entities_df = db.get_atms()['ce_code']
entities = [i for i in entities_df]

entities_percents = [0.0 for _ in entities_df]
entities_intensities = [float(f'{random.random():.3f}') for _ in entities_df]

print(entities_intensities)

start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

date_range = [
    start + datetime.timedelta(days=x)
    for x in range(0, (end-start).days)
]

for date in date_range:
    with open(f'balances/balances.{date}.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['DATE', 'CODE', 'PERCENT'])
        for i in range(len(entities_df)):
            min_range = entities_intensities[i]-random.random()/10
            current_intensity = random.uniform(
                min_range if min_range > 0 else 0,
                entities_intensities[i]+random.random()/10
            )
            temp = entities_percents[i]+current_intensity
            intensity = float(f'{temp:.3f}') if temp < 1 else float(f'{temp-1:.3f}')
            entities_percents[i] = intensity
            writer.writerow([date, entities[i], intensity])
