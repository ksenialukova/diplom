from concurrent.futures import ProcessPoolExecutor, wait
import copy

RS = []
RW = []
RIB = []
s = []


def find_way(ib, X, M, depo):
    costs = copy.deepcopy(M)
    way = [depo, ib]
    S = 0

    for i in X:
        M[i][depo] = float('inf')
        M[i][ib] = float('inf')

    i = way[-1]

    for _ in range(len(X)-1):
        i = way[-1]
        min_index = min(M[i], key=M[i].get)
        way.append(min_index)

        for j in range(len(X)):
            M[X[j]][min_index] = float('inf')

    way.append(depo)

    for i in range(len(way)-1):
        S += costs[way[i]][way[i+1]]

    return S, way, ib


def best_way(M, X, depo):

    with ProcessPoolExecutor(6) as executor:
        tasks = [
            executor.submit(find_way, ib=ib, X=X, M=M, depo=depo)
            for ib in X
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
