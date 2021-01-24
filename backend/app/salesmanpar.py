from concurrent.futures import ProcessPoolExecutor, wait
import copy


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

    print(way)

    return S, way, ib


def best_way(M, X, depo):
    RS = []
    RW = []
    RIB = []
    s = []

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

"""M = {
    2: {2: float('inf'), 4: 8654, 6: 9942, 7: 8694, 9: 8542, 1: 5224},
    4: {2: 6814, 4: float('inf'), 6: 16698, 7: 15450, 9: 14254, 1: 10936},
    6: {2: 11385, 4: 17390, 6: float('inf'), 7: 2105, 9: 5041, 1: 9085},
    7: {2: 9509, 4: 15515, 6: 1701, 7: float('inf'), 9: 4500, 1: 6887},
    9: {2: 8260, 4: 14447, 6: 4697, 7: 3814, 9: float('inf'), 1: 4044},
    1: {2: 7149, 4: 11367, 6: 8753, 7: 6735, 9: 4056, 1: float('inf')}
}

X = [2, 4, 6, 7, 9]
depo = 1

print('neighbours', best_way(M, X, depo))"""
