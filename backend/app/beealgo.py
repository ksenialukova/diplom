import random


def bees_algo(M, X, depo):
    quatilies = []

    scout_bee_count = 30
    selected_bee_count = 5
    best_bee_count = 5
    sel_sites_count = 6
    best_sites_count = 4

    def GenerateWay(X, depo):
        result = [depo]
        random.shuffle(X)
        result += X
        result.append(depo)
        return result

    def GenerateNeighborWay(way):
        way1 = way.copy()
        for i in range(3):
            maximum = 0
            point = 0
            for i in range(1, len(way1)-1):
                if M[way1[i]][way1[i+1]] > maximum:
                    maximum = M[way1[i]][way1[i+1]]
                    point = i

            first_index = point
            second_index = random.randrange(1, len(way1)-1)
            way1[first_index], way1[second_index] = way1[second_index], way1[first_index]
        return way1

    def fitness_func(way):
        S = 0
        for i in range(len(way) - 1):
            S += M[way[i]][way[i + 1]]
        return S

    class Hive:
        def __init__(self,
                     scout_bee_count,
                     selected_bee_count,
                     best_bee_count,
                     sel_sites_count,
                     best_sites_count
                     ):
            self.scout_bee_count = scout_bee_count
            self.selected_bee_count = selected_bee_count
            self.best_bee_count = best_bee_count

            self.sel_sites_count = sel_sites_count
            self.best_sites_count = best_sites_count

            self.best_sites = []
            self.sel_sites = []

            self.beecount = scout_bee_count + selected_bee_count * sel_sites_count + best_bee_count * best_sites_count

            self.swarm = [Bee() for _ in range(self.beecount)]
            self.swarm.sort(key=Bee.bee_sort)

            self.best_position = self.swarm[0].position
            self.best_fitness = self.swarm[0].fitness

        def solve(self):
            cycle = 0
            k = 0
            prev_best = self.best_fitness
            while cycle < 50 and k < 4000:
                quatilies.append(self.best_fitness)

                self.best_sites = self.swarm[0:self.best_sites_count]
                self.sel_sites = self.swarm[self.best_sites_count:self.best_sites_count+self.sel_sites_count]

                bee_index = self.best_sites_count + self.sel_sites_count

                for i in range(len(self.best_sites)):
                    for j in range(self.best_bee_count):
                        """while self.best_sites[i].position in population:
                            self.swarm[bee_index].position = GenerateNeighborWay(self.best_sites[i].position)
                        population.append(self.swarm[bee_index].position)"""
                        self.swarm[bee_index].position = GenerateNeighborWay(
                            self.best_sites[i].position)
                        self.swarm[bee_index].fitness = fitness_func(self.swarm[bee_index].position)
                        bee_index += 1

                for i in range(len(self.sel_sites)):
                    for j in range(self.selected_bee_count):
                        """while self.sel_sites[i].position in population:
                            self.swarm[bee_index].position = GenerateNeighborWay(self.sel_sites[i].position)
                        population.append(self.swarm[bee_index].position)"""
                        self.swarm[bee_index].position = GenerateNeighborWay(
                            self.sel_sites[i].position)
                        self.swarm[bee_index].fitness = fitness_func(self.swarm[bee_index].position)
                        bee_index += 1

                for i in range(bee_index, self.beecount-bee_index) :
                    self.swarm[i] = Bee()

                self.swarm.sort(key=Bee.bee_sort)

                self.best_position = self.swarm[0].position
                self.best_fitness = self.swarm[0].fitness

                if prev_best > self.best_fitness:
                    prev_best = self.best_fitness
                    cycle = 0
                else:
                    cycle += 1

                k += 1

    class Bee:
        def __init__(self):
            """position = GenerateWay(X, depo)
            while position in population:
                position = GenerateWay(X, depo)
            population.append(position)"""
            position = GenerateWay(X, depo)
            fitness = fitness_func(position)

            self.position = position
            self.fitness = fitness

        def bee_sort(self):
            return self.fitness

    hive = Hive(scout_bee_count,
                    selected_bee_count,
                    best_bee_count,
                    sel_sites_count,
                    best_sites_count)

    hive.solve()

    return hive.best_fitness, hive.best_position
