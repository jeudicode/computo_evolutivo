"""
Base Binary Genetic Algorithm


Roulette-based selection
Random mutation
Optional elitism
"""
import matplotlib.pyplot as plt

import random as rand
import math


class BaseGA:

    def __init__(self, init_pop = 2, dim = 1, max_cycles = 1, max_pop_size = 4, mut_rate = 0, opc = 1, elitism = 0):

        rand.seed()

        self.elitism = elitism
        self.max_pop_size = max_pop_size
        self.opc = opc
        self.pop_size = init_pop
        self.dim = dim
        self.mut_rate = mut_rate
        # set max and min values
        if self.opc == 1:
            self.min = -5.12
            self.max = 5.12
            r = (self.max * 2) * 100
            self.length = math.floor(math.log2(r)) * self.dim
        elif self.opc == 2:
            self.min = -5.00
            self.max = 5.00
            r = (self.max * 2) * 100
            self.length = math.floor(math.log2(r)) * 2
        elif self.opc == 3:
            self.min = -512.00
            self.max = 512.00
            r = (self.max * 2) * 100
            self.length = math.floor(math.log2(r)) * 2


        print("len: ", self.length)

        self.max_cycles = max_cycles

        self.count = 0  # benchmark function calls

        if opc == 1:
            self.population = [
                {
                    'genes':
                    [rand.randint(0, 1) for i in range(self.length)],
                    'eval': 0.,
                    'x': [],
                    'prob': 0.,
                    'fitness': 0.
                } for x in range(init_pop)]
        else:
            self.population = [
                {
                    'genes':
                    [rand.randint(0, 1) for i in range(self.length)],
                    'eval': 0.,
                    'x': 0.,
                    'y': 0.,
                    'prob': 0.,
                    'fitness': 0.
                } for x in range(init_pop)]

        self.children = []

        for ind in self.population:
            self.decode(ind)

        self.population = self.eval_pop(self.population)

        print("******** INITIAL POPULATION ********")
        for ind in self.population:
            print(ind)
            # print(str(ind['x']) + " " + str(ind['eval']) + "\n")

    def selection(self):
        total_fitness = 0
        total_prob = 0

        for ind in self.population:
            # print(ind['eval'])
            total_fitness += ind['eval']

        # print("\nTotal fitness: ", total_fitness)

        for ind in self.population:
            prob_ind = ((ind['eval'] / total_fitness))
            ind['prob'] = prob_ind
            total_prob += prob_ind
        
        # print("\n******** Probability Count ********")
        # for ind in self.population:
        #     print(ind)

        self.taken = []

        while len(self.taken) < len(self.population):
            r = rand.random()
            for ind in self.population:
                if r >= ind['prob']:
                    self.taken.append(ind)
                    break
        
        # print("\nTAKEN: \n")
        # for ind in self.taken:
        #     print(ind)


    def crossover(self):
        for ind in self.population:

            # print("current: ", ind)
            partner = 0 # partner to be paired with
            if self.opc == 1:
                first = {
                    'genes': [],
                    'eval': 0.,
                    'x': [],
                    'prob': 0.,
                    'fitness': 0.
                }
                second = {
                    'genes': [],
                    'eval': 0.,
                    'x': [],
                    'prob': 0.,
                    'fitness': 0.
                }
            else:
                first = {
                    'genes': [],
                    'eval': 0.,
                    'x': 0.,
                    'y': 0.,
                    'prob': 0.,
                    'fitness': 0.
                }
                second = {
                    'genes': [],
                    'eval': 0.,
                    'x': 0.,
                    'y': 0.,
                    'prob': 0.,
                    'fitness': 0.
                }

            cross_point = rand.randrange(len(ind['genes']))

            # print("\n crosspoint: ", cross_point)

            first['genes'] += (ind['genes'][0:cross_point])
            first['genes'] += (self.taken[partner]['genes'][cross_point:])

            second['genes'] += (self.taken[partner]['genes'][0:cross_point])
            second['genes'] += (ind['genes'][cross_point:])
            
            if len(self.children) < self.max_pop_size:
                self.children.append(first)
            if len(self.children) < self.max_pop_size:
                self.children.append(second)

            partner += 1

    def mutation(self):
        rate = 1 / self.length
        for child in self.children:
            rand_gene = rand.randrange(self.length)

            r = rand.random()

            if r <= rate:
                if child['genes'][rand_gene] == 1:
                    child['genes'][rand_gene] = 0 
                else:
                    child['genes'][rand_gene] = 1

        for ind in self.children:
            self.decode(ind)

        self.eval_pop(self.children)

    def eval_pop(self, population):
        for i in range(len(population)):
            if self.opc == 1:
                population[i] = self.rastrigin(population[i])
            elif self.opc == 2:
                population[i] = self.himmelblau(population[i])
            elif self.opc == 3:
                population[i] = self.eggholder(population[i])
        
        return population

    def rastrigin(self, individual):
        s = 0
        factor = 10 * self.dim
        for x in individual['x']:
            s += x ** 2 - 10 * math.cos(2 * math.pi * x)

        individual['eval'] = factor + s

        self.count += 1 # update call counter

        if self.count == 20000 or self.count == 20000 or self.count == 20000:
            print("\nThe population: ")
            for ind in self.population:
                print(ind)

        return individual

    def himmelblau(self, individual):
        individual['eval'] = (individual['x'] ** 2 + individual['y'] -
                              11) ** 2 + (individual['x'] + individual['y'] ** 2 - 7) ** 2
        
        self.count += 1 # update call counter


        return individual

    def eggholder(self, individual):

        individual['eval'] = (individual['y'] + 47) * math.sin(math.sqrt(abs((individual['x'] / 2) + (
            individual['y'] + 47)))) - individual['x'] * math.sin(math.sqrt(abs(individual['x'] - (individual['y'] + 47))))
        
        self.count += 1 # update call counter


        return individual

    def decode(self, individual):
        s1 = ""
        s2 = ""
        if self.opc == 1:
            genes = individual['genes']
            #print(genes)
            chunks = [genes[x:x+int(self.length / self.dim)] for x in range(0, len(genes), int(self.length / self.dim))]

            # print(len(chunks))
            for chunk in chunks:
                s1 = ""
                for i in range(len(chunk)):
                    s1 += str(chunk[i])
                x = self.min + 0.01 * int(s1, 2)
                individual['x'].append(x)
        else:
            for i in range(int(len(individual['genes']) / 2)):
                s1 += str(individual['genes'][i])
            for i in range(int(len(individual['genes']) / 2), len(individual['genes'])):
                s2 += str(individual['genes'][i])
            x = self.min + 0.01 * int(s1, 2)
            y = self.min + 0.01 * int(s2, 2)
            individual['x'] = x
            individual['y'] = y

        return individual


def main():

    d = BaseGA(500, 3, 200000, 1000, 0.05, 3)
    g = 0
    while(d.count <= d.max_cycles):
        d.selection()
        d.crossover()
        d.mutation()
        d.population = []
        d.population = d.children
        d.children = []
        g += 1

    print('**** Population after generation %d *****' % (g))
    for ind in d.population:
        print(ind)
        # print(str(ind['x']) + " " + str(ind['eval']) + "\n")



if __name__ == "__main__":
    main()
