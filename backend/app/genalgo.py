import random
import numpy as np
from numpy import exp, sqrt
import matplotlib.pyplot as plt
import time

"""M = {
    2: {2: float('inf'), 4: 8654, 6: 9942, 7: 8694, 9: 8542, 1: 5224},
    4: {2: 6814, 4: float('inf'), 6: 16698, 7: 15450, 9: 14254, 1: 10936},
    6: {2: 11385, 4: 17390, 6: float('inf'), 7: 2105, 9: 5041, 1: 9085},
    7: {2: 9509, 4: 15515, 6: 1701, 7: float('inf'), 9: 4500, 1: 6887},
    9: {2: 8260, 4: 14447, 6: 4697, 7: 3814, 9: float('inf'), 1: 4044},
    1: {2: 7149, 4: 11367, 6: 8753, 7: 6735, 9: 4056, 1: float('inf')}
}

X = [2, 4, 6, 7, 9]
depo = 1"""

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

# x = [10, 60, 100, 100, 30, 20, 20, 50, 50, 85]
# y = [5, 40, 0, 90, 50, 55, 50, 75, 25, 50]
# n = len(x)

n = 20
m = 100
a = 0
x = np.random.uniform(a, m, n)
y = np.random.uniform(a, m, n)


M = {}
for i in np.arange(0, n, 1):
    M[i] = {}
    for j in np.arange(0, n, 1):
        if i != j:
            M[i][j] = sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)
        else:
            M[i][j] = float('inf')

X = [i for i in range(1, n)]

depo = 0

quatilies = []

totalNumberBees = 100
numberInactive = 20
numberActive = 50
numberScout = 30
maxNumberVisits = 1000
maxNumberCycles = 100000

start = time.monotonic()

def GenerateWay(X, depo):
    result = [depo]
    random.shuffle(X)
    result += X
    result.append(depo)
    return result


def MeasureOfQuality(way):
    S = 0
    for i in range(len(way) - 1):
        S += M[way[i]][way[i + 1]]
    return S


class Hive:
    def __init__(self,
                 totalNumberBees,
                 numberInactive,
                 numberActive,
                 numberScout,
                 maxNumberCycles,
                 maxNumberVisits):

        self.probPersuasion = 0.90
        self.probMistake = 0.01
        self.totalNumberBees = totalNumberBees
        self.numberInactive = numberInactive
        self.numberActive = numberActive
        self.numberScout = numberScout
        self.maxNumberCycles = maxNumberCycles
        self.maxNumberVisits = maxNumberVisits
        self.bestMemoryMatrix = GenerateWay(X, depo)
        self.indexesOfInactiveBees = []
        self.bestMeasureOfQuality = MeasureOfQuality(self.bestMemoryMatrix)
        self.bees = []

        for i in range(self.totalNumberBees):
            if i < self.numberInactive:
                currStatus = 0  # inactive
                self.indexesOfInactiveBees.append(i)
            elif i < self.numberInactive + self.numberScout:
                currStatus = 2  # scout
            else:
                currStatus = 1  # active

            randomMemoryMatrix = GenerateWay(X, depo)
            mq = MeasureOfQuality(randomMemoryMatrix)
            numberOfVisits = 0
            self.bees.append(Bee(currStatus, randomMemoryMatrix, mq, numberOfVisits))

            if self.bees[len(self.bees)-1].measureOfQuality < self.bestMeasureOfQuality:
                self.bestMemoryMatrix = self.bees[len(self.bees)-1].memoryMatrix
                self.bestMeasureOfQuality = self.bees[
                    len(self.bees) - 1].measureOfQuality


class Bee:
    def __init__(self,
                 status,
                 memoryMatrix,
                 measureOfQuality,
                 numberOfVisits):
        self.status = status
        self.memoryMatrix = memoryMatrix
        self.measureOfQuality = measureOfQuality
        self.numberOfVisits = numberOfVisits


hive = Hive(totalNumberBees, numberInactive, numberActive, numberScout, maxNumberVisits, maxNumberCycles)


def GenerateNeighborWay(way):
    first_index = random.randrange(0, len(way))
    if first_index == len(way) - 1:
        second_index = 0
    else:
        second_index = first_index + 1

    way[first_index], way[second_index] = way[second_index], way[first_index]
    return way


def solve(hive):
    cycle = 0
    while cycle < hive.maxNumberCycles:
        for i in range(hive.totalNumberBees):
            if hive.bees[i].status == 1:
                ProcessActiveBee(i)
            elif hive.bees[i].status == 2:
                ProcessScoutBee(i)
            elif hive.bees[i].status == 0:
                ProcessInactiveBee(i)
        cycle += 1


def ProcessActiveBee(i):
    bee = hive.bees[i]

    neighbour = GenerateNeighborWay(bee.memoryMatrix)
    neighbourQuality = MeasureOfQuality(neighbour)

    prob = random.random()
    memoryWasUpdated = False
    numberOfVisitsOverLimit = False

    if neighbourQuality < bee.measureOfQuality:  # better
        if prob < hive.probMistake:  # mistake
            bee.numberOfVisits += 1
            if bee.numberOfVisits > hive.maxNumberVisits:
                numberOfVisitsOverLimit = True
        else:  # No mistake
            bee.memoryMatrix = neighbour
            bee.numberOfVisits = 0
            memoryWasUpdated = True
    else:  # Did not find better neighbor
        if prob < hive.probMistake:  # mistake
            bee.memoryMatrix = neighbour
            bee.numberOfVisits = 0
            memoryWasUpdated = True
        else:
            bee.numberOfVisits += 1
            if bee.numberOfVisits > hive.maxNumberVisits:
                numberOfVisitsOverLimit = True

    if numberOfVisitsOverLimit:
        bee.status = 0
        bee.numberOfVisits = 0
        x = random.randrange(hive.numberInactive)
        hive.bees[hive.indexesOfInactiveBees[x]].status = 1
        hive.indexesOfInactiveBees[x] = i
    elif memoryWasUpdated:
        if bee.measureOfQuality < hive.bestMeasureOfQuality:
            hive.bestMemoryMatrix = bee.memoryMatrix
            hive.bestMeasureOfQuality = bee.measureOfQuality

        DoWaggleDance(i)


def ProcessScoutBee(i):
    randomFoodSource = GenerateWay(X, depo)
    randomFoodSourceQuality = MeasureOfQuality(randomFoodSource)
    if randomFoodSourceQuality < hive.bees[i].measureOfQuality:
        hive.bees[i].memoryMatrix = randomFoodSource
        hive.bees[i].measureOfQuality = randomFoodSourceQuality
        if hive.bees[i].measureOfQuality < hive.bestMeasureOfQuality:
            hive.bestMemoryMatrix = hive.bees[i].memoryMatrix
            hive.bestMeasureOfQuality = hive.bees[i].measureOfQuality

        DoWaggleDance(i)


def ProcessInactiveBee(i):
    pass


def DoWaggleDance(i):
    bee = hive.bees[i]
    for ii in range(hive.numberInactive):
        b = hive.indexesOfInactiveBees[ii]
        if bee.measureOfQuality < hive.bees[b].measureOfQuality:
            p = random.random()
            if hive.probPersuasion > p:
                hive.bees[b].memoryMatrix = bee.memoryMatrix
                hive.bees[b].measureOfQuality = bee.measureOfQuality


solve(hive)
print(hive.bestMeasureOfQuality, len(hive.bestMemoryMatrix))

end = time.monotonic()
# print(end - start)

# X1 = [x[hive.bestMemoryMatrix[i]] for i in np.arange(0, n, 1)]
# Y1 = [y[hive.bestMemoryMatrix[i]] for i in np.arange(0, n, 1)]

"""plt.xlabel('Координата Х')
plt.ylabel('Координата Y')
plt.plot(X1, Y1, color='b', linestyle=' ', marker='o')
plt.plot(X1, Y1, color='g', linewidth=1)
X2 = [x[hive.bestMemoryMatrix[n-2]], x[hive.bestMemoryMatrix[n-1]]]
Y2 = [y[hive.bestMemoryMatrix[n-2]], y[hive.bestMemoryMatrix[n-1]]]
plt.plot(X2, Y2, color='r', linewidth=2,  linestyle='-', label='Шлях від останнього \n до першого пункту')
plt.legend(loc='best')
plt.grid(True)
plt.show()"""

# print(quatilies)
# quatilies = [25291.45546417859, 25087.048398994666, 25087.048398994666, 25087.048398994666, 25087.048398994666, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24843.72903061716, 24627.097324512673, 24627.097324512673, 24627.097324512673, 24627.097324512673, 24627.097324512673, 24627.097324512673, 24627.097324512673, 24627.097324512673, 24627.097324512673, 24627.097324512673]


"""plt.xlabel('Ітерація')
plt.ylabel('Значення')
plt.plot([i for i in range(len(quatilies))], quatilies, color='r', linewidth=1)
plt.grid(True)
plt.show()"""


# bees = [4453.573089907798, ]

print('neighbours', best_way(M, X, depo)[0], len(best_way(M, X, depo)[2]))
