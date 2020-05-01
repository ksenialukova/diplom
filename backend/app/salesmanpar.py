from concurrent.futures import ProcessPoolExecutor, wait
import numpy as np
from numpy import sqrt

RS = []
RW = []
RIB = []
s = []


def find_way(ib, n, X, Y, M):
    way = list()
    way.append(ib)
    for i in np.arange(1, n, 1):
        s = []
        for j in np.arange(0, n, 1):
            s.append(M[way[i - 1], j])
        way.append(s.index(min(s)))
        for j in np.arange(0, i, 1):
            M[way[i], way[j]] = float('inf')
            M[way[i], way[j]] = float('inf')
    S = sum([sqrt(
        (X[way[i]] - X[way[i + 1]]) ** 2 + (Y[way[i]] - Y[way[i + 1]]) ** 2)
        for i in np.arange(0, n - 1, 1)]) + sqrt(
        (X[way[n - 1]] - X[way[0]]) ** 2 + (Y[way[n - 1]] - Y[way[0]]) ** 2)

    return S, way, ib


def best_way(n, X, Y):
    M = np.zeros([n, n])
    for i in np.arange(0, n, 1):
        for j in np.arange(0, n, 1):
            if i != j:
                M[i, j] = sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
            else:
                M[i, j] = float('inf')

    with ProcessPoolExecutor(6) as executor:
        tasks = [
            executor.submit(find_way, ib=ib, n=n, X=X, Y=Y, M=M)
            for ib in np.arange(0, n, 1)
        ]
        # we must wait until the whole layer processing finished:
        wait(tasks)

    for i in range(len(tasks)):
        RS.append(tasks[i].result()[0])
        RW.append(tasks[i].result()[1])
        RIB.append(tasks[i].result()[2])

    S = min(RS)
    result_way = RW[RS.index(min(RS))]
    ib = RIB[RS.index(min(RS))]

    return S, ib, result_way
