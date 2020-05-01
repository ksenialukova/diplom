import datetime
import csv
import random

start_date = '2020-03-01'
end_date = '2020-03-31'

entity_number = 8
entities = [f'{i+2}' for i in range(entity_number)]

entities_percents = [0.0 for _ in range(entity_number)]
entities_intensities = [float(f'{random.random()/2:.3f}') for _ in range(entity_number)]

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
        for i in range(entity_number):
            current_intensity = random.uniform(
                entities_intensities[i]-random.random()/10,
                entities_intensities[i]+random.random()/10
            )
            temp = entities_percents[i]+current_intensity
            intensity = float(f'{temp:.3f}') if temp < 1 else float(f'{temp-1:.3f}')
            entities_percents[i] = intensity
            writer.writerow([date, entities[i], intensity])
