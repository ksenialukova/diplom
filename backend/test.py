n = [8, 9, 10, 11, 12]
time_bees = [0.139, 0.140, 0.1631, 0.166, 0.1735]
time_neighbours = [0.0267, 0.0261, 0.0327, 0.0271, 0.0281]
time_all = [0.0355, 0.261, 2.489, 26.7674, 335.048]

result_bees = [295.9354, 318.686, 301.599, 283.662, 334.880]
result_neighbours = [326.9829, 334.160, 326.057, 289.153, 360.337]
result_all = [295.9354, 311.055, 298.808, 257.188, 300.875]

import numpy as np
import matplotlib.pyplot as plt

width = 0.1
x = np.arange(len(n))

"""

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)

ax.set_xlabel('Координата Х')
ax.set_ylabel('Координата Y')
ax.set_xticklabels([0]+n)
# rects = ax.bar(x-width, result_bees, width, label='Метод бджолиних колоній')
# rects1 = ax.bar(x, result_neighbours, width, label='Метод найближчого сусіда')
# rects2 = ax.bar(x+width, result_all, width, label='Метод повного перебору')

ax.plot(x, time_bees, label='Метод бджолиних колоній')
ax.legend(loc='best')
ax.set_title('Час від кількості пунктів')

for rect in rects+rects1+rects2:
    height = rect.get_height()
    label = ax.annotate(height,
                        xy=(rect.get_x(), height),
                        xytext=(5, 0),
                        textcoords="offset points",
                        weight='bold',
                        rotation=60
                        )

plt.show()"""

plt.xlabel('Координата Х')
plt.ylabel('Координата Y')
plt.xticks(n)
plt.plot(n, time_bees, color='b', linewidth=1, label='Метод бджолиних колоній')
plt.plot(n, time_all, color='r', linewidth=1, label='Метод бджолиних колоній')
plt.plot(n, time_neighbours, color='g', linewidth=1, label='Метод бджолиних колоній')
plt.legend(loc='best')
plt.show()

plt.xlabel('Координата Х')
plt.ylabel('Координата Y')
plt.xticks(n)
plt.plot(n, time_all, color='r', linewidth=1, label='Метод бджолиних колоній')
plt.legend(loc='best')
plt.show()

plt.xlabel('Координата Х')
plt.ylabel('Координата Y')
plt.xticks(n)
plt.plot(n, time_neighbours, color='g', linewidth=1, label='Метод бджолиних колоній')
plt.legend(loc='best')
plt.show()


"""start = time.monotonic()
res = best_way(M, X, depo)

print('neighbours', res[0], res[2])
end = time.monotonic()
print('neighbours', end - start)


X1 = [x[res[2][i]] for i in np.arange(0, n, 1)]
Y1 = [y[res[2][i]] for i in np.arange(0, n, 1)]
X2 = [x[res[2][n-1]], x[res[2][n]]]
Y2 = [y[res[2][n-1]], y[res[2][n]]]

ax1.set_xlabel('Координата Х')
ax1.set_ylabel('Координата Y')
ax1.plot(X1, Y1, color='b', linestyle=' ', marker='o')
ax1.plot(X1, Y1, color='g', linewidth=1)
ax1.plot(X2, Y2, color='r', linewidth=2,  linestyle='-', label='Шлях від останнього \n до першого пункту')
ax1.set_title(f'Метод найближчих сусідів\n(довжина шляху = {res[0]:.2f})')"""

"""plt.xlabel('Координата Х')
plt.ylabel('Координата Y')
plt.plot(X1, Y1, color='b', linestyle=' ', marker='o')
plt.plot(X1, Y1, color='g', linewidth=1)
X2 = [x[res[2][n-1]], x[res[2][n]]]
Y2 = [y[res[2][n-1]], y[res[2][n]]]
plt.plot(X2, Y2, color='r', linewidth=2,  linestyle='-', label='Шлях від останнього \n до першого пункту')
plt.legend(loc='best')
plt.grid(True)
plt.show()"""


"""min_way = []
min_cost = float('inf')

import itertools
start = time.monotonic()
for i in itertools.permutations(X):
    S = 0
    res = [depo]
    res += i
    res.append(depo)
    for i in range(len(res)-1):
        S += M[res[i]][res[i+1]]

    if min_cost > S:
        min_way = res
        min_cost = S
print('all', min_cost, min_way)
end = time.monotonic()
print('all', end-start)

X1 = [x[min_way[i]] for i in np.arange(0, n, 1)]
Y1 = [y[min_way[i]] for i in np.arange(0, n, 1)]
X2 = [x[min_way[n-1]], x[min_way[n]]]
Y2 = [y[min_way[n-1]], y[min_way[n]]]"""

"""ax2.set_xlabel('Координата Х')
ax2.set_ylabel('Координата Y')
ax2.plot(X1, Y1, color='b', linestyle=' ', marker='o')
ax2.plot(X1, Y1, color='g', linewidth=1)
ax2.plot(X2, Y2, color='r', linewidth=2,  linestyle='-', label='Шлях від останнього \n до першого пункту')
ax2.set_title(f'Повний перебір\n(довжина шляху = {min_cost:.2f})')
"""
"""plt.xlabel('Координата Х')
plt.ylabel('Координата Y')
plt.plot(X1, Y1, color='b', linestyle=' ', marker='o')
plt.plot(X1, Y1, color='g', linewidth=1)
X2 = [x[min_way[n-1]], x[min_way[n]]]
Y2 = [y[min_way[n-1]], y[min_way[n]]]
plt.plot(X2, Y2, color='r', linewidth=2,  linestyle='-', label='Шлях від останнього \n до першого пункту')
plt.legend(loc='best')
plt.grid(True)
plt.show()"""


# plt.show()
