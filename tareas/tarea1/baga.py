#!/usr/bin/env python

"""
Base Binary Genetic Algorithm


Roulette-based selection
Random mutation
Optional elitism
"""
#import matplotlib.pyplot as plt

import random as rand
import math
# import matplotlib.pyplot as plt
import csv


class BaseGA:

    def __init__(self, init_pop = 2, dim = 1, max_cycles = 1, opc = 1):

        rand.seed()

        self.best = []

        #self.max_pop_size = max_pop_size
        self.opc = opc
        self.pop_size = init_pop
        self.dim = dim
        # set max and min values
        if self.opc == 1:
            self.min = -5.12
            self.max = 5.12
            r = (self.max * 2) * 10000
            self.length = math.floor(math.log2(r)) * self.dim
        elif self.opc == 2:
            self.min = -5.00
            self.max = 5.00
            r = (self.max * 2) * 10000
            self.length = math.floor(math.log2(r)) * 2
        elif self.opc == 3:
            self.min = -512.00
            self.max = 512.00
            r = (self.max * 2) * 10000
            self.length = math.floor(math.log2(r)) * 2

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

        aux = self.population.copy()

        def getF(elem):
            return elem['fitness']
        
        aux.sort(key=getF, reverse=True)

        self.best.append(aux[0])

        print("******** INITIAL POPULATION ********")
        for ind in self.population:
            # print(ind)
            print(str(ind['x']) + " " + str(ind['eval']) + " " + str(ind['fitness']) + "\n")

    def selection(self):

        self.selected = []

        # roulette selection
        # total_fitness = 0
        # total_prob = 0

        # for ind in self.population:
        #     total_fitness += ind['fitness']

        # rel = [ind['fitness']/total_fitness for ind in self.population]
        # probs = [sum(rel[:i+1]) for i in range(len(rel))]

        # while len(self.selected) < len(self.population):
        #     r = rand.random()
        #     for (i, ind)in enumerate(self.population):
        #         if r <= probs[i]:
        #             self.selected.append(ind)
        #             break

        ########### Tournament selection
        # for i in range(len(self.population)):
        #     r = rand.randrange(0, len(self.population))
        #     if self.population[i]['fitness'] >= self.population[r]['fitness']:
        #         self.selected.append(self.population[i])
        #     else:
        #         self.selected.append(self.population[r])

        ########## Stochastic Universal Sampling
        total_fitness = 0

        for ind in self.population:
            total_fitness += ind['fitness']

        n = 10 # individuals to keep
        p = self.length - n # distance
        start = rand.randrange(0, p)
        pointers = [start + i * p for i in range(n)]
        c = [sum(self.population[:i+1]['fitness']) for i in range(len(rel))]
        
        self.selected = rws(self.population, pointers)
        
        def rws(population, points):
            keep = []
            for p in points:
                i = 0
                while c[i] < p:
                    i += 1
                keep.append(population[i])
            return keep
            



        # Vasconcelos method

    def crossover(self):
        for (i, ind) in enumerate(self.selected):

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

            if i % 2 == 0:
                partner = i + 1
            else: 
                partner = i -1
            
            if i == len(self.selected) - 1:
                partner = 0

            first['genes'] += (ind['genes'][0:cross_point])
            first['genes'] += (self.selected[partner]['genes'][cross_point:self.length])

            second['genes'] += (self.selected[partner]['genes'][0:cross_point])
            second['genes'] += (ind['genes'][cross_point:self.length])
            
            if len(self.children) < self.pop_size:
                self.children.append(first)
            if len(self.children) < self.pop_size:
                self.children.append(second)

    def mutation(self):
        rate = 0.1 / self.length
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


        def getF(elem):
            return elem['fitness']

        # elitism
        aux1 = self.population.copy()
        aux1.sort(key=getF, reverse=True)

        elite = aux1[:9]


        aux = self.children.copy()
        aux.sort(key=getF, reverse=True)
        elite_c = aux[:90]

        new_pop = elite + elite_c
        self.population = new_pop.copy()

        self.best.append(aux[0])

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

        individual['fitness'] = 1 / (individual['eval'] + 0.00001) 

        self.count += 1 # update call counter

        return individual

    def himmelblau(self, individual):
        individual['eval'] = (individual['x'] ** 2 + individual['y'] -
                              11) ** 2 + (individual['x'] + individual['y'] ** 2 - 7) ** 2

        individual['fitness'] = 1 / individual['eval']
        
        self.count += 1 # update call counter


        return individual

    def eggholder(self, individual):

        individual['eval'] = (individual['y'] + 47) * math.sin(math.sqrt(abs((individual['x'] / 2) + (
            individual['y'] + 47)))) - individual['x'] * math.sin(math.sqrt(abs(individual['x'] - (individual['y'] + 47))))

         
        individual['fitness'] = -individual['eval']
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
                x = self.min + 0.0001 * int(s1, 2)
                individual['x'].append(x)
        else:
            for i in range(int(len(individual['genes']) / 2)):
                s1 += str(individual['genes'][i])
            for i in range(int(len(individual['genes']) / 2), len(individual['genes'])):
                s2 += str(individual['genes'][i])
            x = self.min + 0.0001 * int(s1, 2)
            y = self.min + 0.0001 * int(s2, 2)
            individual['x'] = x
            individual['y'] = y

        return individual


def main():

    d = BaseGA(100, 2, 500, 1)
    g = 0
    while(g < d.max_cycles):
        d.selection()
        d.crossover()
        d.mutation()
        # d.population = []
        # d.population = d.children
        d.children = []
        g += 1

    print('***** Best solutions after %d *****' % (g))
    for ind in d.best:
        print(str(ind['eval']) + " " + str(ind['fitness']) + "\n")
    
    # with open('results_elite_sus_'+str(d.opc)+'.csv', mode='w') as res_file:
    #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    #     res_writer.writerow(['eval', 'fitness'])
    #     for ind in d.best:
    #         res_writer.writerow([ind['eval'], ind['fitness']])




if __name__ == "__main__":
    main()
