import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([
     [0.1, 0.4, 0.6, 0.8, 0.2, 0.4, 0.6, 0.8, 0.3],
     [0.3, 0.6, 0.9, 0.2, 0.1, 0.3, 0.6, 0.9, 0.2]
])

y = np.array([0.5, 0.7])

x1 = [[0.5, 0.9, 0.3, 0.8, 0.2, 0.5, 0.8, 0.3, 0.7]]

model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)


y_pred = model.predict(x1)
print(y_pred)
