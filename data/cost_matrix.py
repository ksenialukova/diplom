import pandas as pd
import googlemaps

API_key = 'AIzaSyAjJiOQYpv9x7CWjzfcHFkRPmMJBTy_3C0'
gmaps = googlemaps.Client(key=API_key)

df = pd.read_csv('../data/cash_entities/cash_entities.csv')

distance_df = pd.DataFrame({
    'FROM_CODE': [],
    'TO_CODE': [],
    'DISTANCE': [],
    'DURATION': []
})

origin_codes = []
dest_codes = []
distances = []
durations = []

for origin_index, origin_row in df.iterrows():
    origin_code = origin_row['CODE']
    origin_lat = origin_row['X_COORD']
    origin_lng = origin_row['Y_COORD']

    for dest_index, dest_row in df.iterrows():
        dest_code = dest_row['CODE']
        dest_lat = dest_row['X_COORD']
        dest_lng = dest_row['Y_COORD']

        result = gmaps.distance_matrix((origin_lat, origin_lng),
                                       (dest_lat, dest_lng),
                                       mode='driving')

        distance = result['rows'][0]['elements'][0]['distance']['value']
        duration = result['rows'][0]['elements'][0]['duration']['value']

        origin_codes.append(origin_code)
        dest_codes.append(dest_code)
        distances.append(distance)
        durations.append(duration)

distance_df['FROM_CODE'] = origin_codes
distance_df['TO_CODE'] = dest_codes
distance_df['DISTANCE'] = distances
distance_df['DURATION'] = durations
distance_df.to_csv('distances/distances.csv', sep=',', index=None)
