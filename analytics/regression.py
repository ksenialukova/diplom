import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([
     [6, 6, 7],
     [2, 2, 2],
     [3, 2, 2],
     [3, 2, 3],
     [5, 5, 5]])

y = np.array([7, 2, 2, 2, 6])

x1 = [[3, 2, 4]]
y1 = [2]

model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)


y_pred = model.predict(x1)
