#!/usr/bin/env python

"""
Base Genetic Algorithm with Real Encoding


Roulette-based selection
Random mutation
Optional elitism
"""
import test_functions as bench
import random as rand
import math
# import matplotlib.pyplot as plt
import csv


class RealGA:

    # n is only for n-queens problem and tsp

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
        elif self.opc == 2:
            self.min = -5.00
            self.max = 5.00
        elif self.opc == 3:
            self.min = -512.00
            self.max = 512.00
        elif self.opc == 4:
            self.min = 0
            self.max = self.dim - 1
        elif self.opc == 5:
            self.min = 0
            self.max = self.dim - 1

        self.max_cycles = max_cycles

        self.count = 0  # benchmark function calls

        if(self.opc < 4):
            if self.opc == 1:
                self.population = [
                    {
                        'genes':
                        [round(rand.uniform(self.min, self.max), 2) for i in range(self.dim)],
                        'eval': 0.,
                        'x': [round(rand.uniform(self.min, self.max), 2) for i in range(self.dim)],
                        'prob': 0.,
                        'fitness': 0.
                    } for x in range(init_pop)
                ]
            else:
                self.population = [
                    {
                        'genes':
                        [round(rand.uniform(self.min, self.max), 2) for i in range(self.dim)],
                        'eval': 0.,
                        'x': [round(rand.uniform(self.min, self.max), 2) for i in range(self.dim)],
                        'prob': 0.,
                        'fitness': 0.
                    } for x in range(init_pop)
                ]
        else:
            self.population = [
                {
                    'genes': [],
                    'eval': 0.,
                    'x': [round(rand.uniform(self.min, self.max), 2) for i in range(self.dim)],
                    'prob': 0.,
                    'fitness': 0.
                } for x in range(init_pop)
            ]

            r = round(rand.uniform(0, self.dim), 2)
            
            for ind in self.population:
                for i in range(self.dim):
                    if r not in ind['x']:
                        ind['x'].append(r)
                    else:
                        while r in ind['x']:
                            r = round(rand.uniform(0, self.dim-1), 2)
                        ind['x'].append(r)
               
        self.children = []

        self.population = self.eval_pop(self.population)

        aux = self.population.copy()
        
        aux.sort(key=self.getFitness, reverse=True)

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
        for i in range(len(self.population)):
            r = rand.randrange(0, len(self.population))
            if self.population[i]['eval'] <= self.population[r]['eval']:
                self.selected.append(self.population[i])
            else:
                self.selected.append(self.population[r])

        ########## Stochastic Universal Sampling
        # total_fitness = 0
      
        # sums = []
        # s = 0
        # for ind in self.population:
        #     total_fitness += ind['fitness']
        #     if len(sums) > 1:
        #         s = sums[len(sums) - 1] + ind['fitness']
        #         sums.append(s)
        #     else:
        #         sums.append(ind['fitness'])

        # point_distance = int(total_fitness / self.dim)
        # start_point = int(rand.uniform(0, point_distance))
        # points = [start_point + i * point_distance for i in range(self.dim)]
        # while len(self.selected) < self.dim:
        #     # rand.shuffle(self.population)
        #     i = 0
        #     while i < len(points) and len(self.selected) < self.dim:
        #         j = 0
        #         while j < len(self.population):
        #             if sums[j] > points[i]:
        #                 self.selected.append(self.population[j])
        #                 break
        #             j += 1
        #         i += 1
        
        # Vasconcelos method
        # def getFitness(elem):
        #     return elem['fitness']

        # aux1 = self.population.copy()
        # aux1.sort(key=getFitness, reverse=True)

        # self.selected = aux1.copy()

    def crossover(self):

            for (i, ind) in enumerate(self.selected):
                if self.opc >= 4:
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
                elif self.opc == 1:
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
                        'x': [0,0],
                        'prob': 0.,
                        'fitness': 0.
                    }
                    second = {
                        'genes': [],
                        'eval': 0.,
                        'x': [0,0],
                        'prob': 0.,
                        'fitness': 0.
                    }

                if self.opc < 4:

                    cross_point = rand.randrange(self.dim)

                    # fol all methods except Vasconcelos
                    if i % 2 == 0:
                        partner = i + 1
                    else: 
                        partner = i -1
                    
                    if i == len(self.selected) - 1:
                        partner = 0

                    # for Vasconcelos only
                    #partner = (len(self.population) - 1) - i

                    first['x'] += (ind['x'][0:cross_point])
                    first['x'] += (self.selected[partner]['x'][cross_point:self.dim])

                    second['x'] += (self.selected[partner]['x'][0:cross_point])
                    second['x'] += (ind['x'][cross_point:self.dim])
                    
                    if len(self.children) < self.pop_size:
                        self.children.append(first)
                    if len(self.children) < self.pop_size:
                        self.children.append(second)
                
                else:

                    # fol all methods except Vasconcelos
                    if i % 2 == 0:
                        partner = i + 1
                    else: 
                        partner = i -1
                    
                    if i == len(self.selected) - 1:
                        partner = 0

                    # for Vasconcelos only
                    #partner = (len(self.population) - 1) - i

                    start = rand.randrange(0, self.dim - 1)
                    end = rand.randrange(start + 1, self.dim)

                    first['x'] = ind['x'][start:end]

                    for i in range(self.dim):
                        elem = self.selected[partner]['x'][i]
                        if(elem not in first['x']):
                            first['x'].append(elem)

                    #print(first)
                    
                    if len(self.children) < self.pop_size:
                        self.children.append(first)


    def mutation(self):
        rate = 0.1 / self.dim
        for child in self.children:
            rand_gene = rand.randrange(0, self.dim)

            r = rand.random()

            if self.opc < 4:
                if r <= rate:
                    child['x'][rand_gene] = round(rand.uniform(self.min, self.max), 2)
            else:
                if r <= rate:
                    indexA = rand.randrange(self.dim - 1)
                    indexB = indexA + 1
                    child['x'][indexA], child['x'][indexB] = child['x'][indexB], child['x'][indexA]
                  

        self.eval_pop(self.children)


    def getFitness(self, elem):
        #return elem['eval']
        return elem['fitness']

    def elitism(self):
        # elitism
        aux1 = self.population.copy()
        aux1.sort(key=self.getFitness, reverse=True)

        elite = aux1[:9]

        aux = self.children.copy()
        aux.sort(key=self.getFitness, reverse=True)
        elite_c = aux[:90]

        new_pop = elite + elite_c
        self.population = new_pop.copy()
        new_pop.sort(key=self.getFitness, reverse=True)
        self.best.append(new_pop[0])

    def eval_pop(self, population):
        for i in range(len(population)):
            if self.opc == 1:
                population[i] = bench.rastrigin(population[i])
            elif self.opc == 2:
                population[i] = bench.himmelblau(population[i])
            elif self.opc == 3:
                population[i] = bench.eggholder(population[i])
            elif self.opc == 4:
                population[i] = bench.nqueens(population[i])
            elif self.opc == 5:
                population[i] = bench.tsp(population[i])
            
            self.count += 1
        
        return population

def main():

    d = RealGA(100, 2, 300, 2)
    g = 0
    while(g < d.max_cycles):
        d.selection()
        d.crossover()
        d.mutation()
        d.elitism()
        d.children = []
        g += 1

    print('***** Best solutions after %d *****' % (g))
    for ind in d.best:
        print(str(ind['x']) + " " + str(ind['eval']) + " " + str(ind['fitness']) + "\n")
    
    with open('res_real_today_'+str(d.opc)+'_10.csv', mode='w') as res_file:
        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        res_writer.writerow(['x1','eval'])
        for ind in d.best:
            res_writer.writerow([ind['x'], ind['eval']])

if __name__ == "__main__":
    main()
