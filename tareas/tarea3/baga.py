#!/usr/bin/env python

"""
Base Binary Genetic Algorithm


Roulette-based selection
Random mutation
Optional elitism
"""
#import matplotlib.pyplot as plt
import test_functions as bench
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
        elif self.opc == 4:
            self.min = 0
            self.max = self.dim
            f = math.factorial(self.max )
            self.length = math.ceil(math.log2(f))
        elif self.opc == 5:
            self.min = 0
            self.max = self.dim
            f = math.factorial(self.max)
            self.length = math.ceil(math.log2(f))
        
        print(self.length)

        self.max_cycles = max_cycles

        self.count = 0  # benchmark function calls

        if self.opc == 1:
            self.population = [
                {
                    'genes':[rand.randint(0, 1) for i in range(self.length)],
                    'eval': 0.,
                    'x': [],
                    'prob': 0.,
                    'fitness': 0.
                } for x in range(init_pop)]
        elif self.opc > 1 and self.opc < 4:
            self.population = [
                {
                    'genes':[rand.randint(0, 1) for i in range(self.length)],
                    'eval': 0.,
                    'x': [0, 0],
                    'prob': 0.,
                    'fitness': 0.
                } for x in range(init_pop)]
        else:
             self.population = [
                {
                    'genes':[rand.randint(0, 1) for i in range(self.length)],
                    'eval': 0.,
                    'x': [],
                    'prob': 0.,
                    'fitness': 0.
                } for x in range(init_pop)]
       

        self.children = []

        # for ind in self.population:
        #     print(ind['genes'])

        for ind in self.population:
            self.decode(ind)

        self.population = self.eval_pop(self.population)

        aux = self.population.copy()
        
        aux.sort(key=self.getFitness, reverse=True)

        self.best.append(aux[0])

        print("******** INITIAL POPULATION ********")
        for ind in self.population:
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
            # if self.population[i]['fitness'] >= self.population[r]['fitness']:
            #     self.selected.append(self.population[i])
            # else:
            #     self.selected.append(self.population[r])

            if self.population[i]['fitness'] >= self.population[r]['fitness']:
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

        # point_distance = int(total_fitness / self.length)
        # start_point = int(rand.uniform(0, point_distance))
        # points = [start_point + i * point_distance for i in range(self.length)]
        # while len(self.selected) < self.length:
        #     # rand.shuffle(self.population)
        #     i = 0
        #     while i < len(points) and len(self.selected) < self.length:
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

            cross_point = rand.randrange(len(ind['genes']))
         
            # fol all methods except Vasconcelos
            if i % 2 == 0:
                partner = i + 1
            else: 
                partner = i -1
            
            if i == len(self.selected) - 1:
                partner = 0

            # for Vasconcelos only
            #partner = (len(self.population) - 1) - i

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
    
    def getFitness(self, elem):
        return elem['fitness']
        #return elem['eval']

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

    
    def decode(self, individual):
        s1 = ""
        s2 = ""
        if self.opc == 1:
            genes = individual['genes']
            #print(genes)
            chunks = [genes[x:x+int(self.length / self.dim)] for x in range(0, len(genes), int(self.length / self.dim))]

            for chunk in chunks:
                s1 = ""
                for i in range(len(chunk)):
                    s1 += str(chunk[i])
                x = self.min + 0.01 * int(s1, 2)
                individual['x'].append(x)
        elif self.opc > 1 and self.opc < 4:
            for i in range(int(len(individual['genes']) / 2)):
                s1 += str(individual['genes'][i])
            for i in range(int(len(individual['genes']) / 2), len(individual['genes'])):
                s2 += str(individual['genes'][i])

            x = self.min + 0.01 * int(s1, 2)
            y = self.min + 0.01 * int(s2, 2)
            individual['x'][0] = x
            individual['x'][1] = y
        
        else:
            l = [i for i in range(self.max)]
            #print(l)
            f = math.factorial(self.max - 1)
            genes = individual['genes']
            strings = [str(x) for x in genes]
            a_string = "".join(strings)
            n = int(a_string, 2)
            individual['x'] = []
             

            # repairing
            if n >= f:
                for i in range(self.length):
                    if individual['genes'][i] == 0:
                        individual['genes'][i] = 1
                    else:
                        individual['genes'][i] = 0
                #individual['genes'][0] = 0
                genes = individual['genes']
                strings = [str(x) for x in genes]
                a_string = "".join(strings)
                n = int(a_string, 2)
            
            #print(a_string + " " + str(n))
            m = self.max - 1
            for i in range(m):
                if (len(l) > 1):
                    q = int(n / math.factorial(m - i)) 
                    if q >= len(l):
                        q = len(l) - q
                    #print(str(n) + " " + str(q) + " " + str(len(l)))
                    r = n % math.factorial(m - i)
                    x = l[q]
                    l.remove(x)
                    individual['x'].append(x)
                    n = r
                else:
                    individual['x'].append(l[0])
                



        return individual


def main():

    d = BaseGA(100, 2, 300, 2)
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
    
    with open('res_bin_today_'+str(d.opc)+'_10.csv', mode='w') as res_file:
        res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        res_writer.writerow(['x','eval', 'fitness'])
        for ind in d.best:
            res_writer.writerow([ind['x'], ind['eval'], ind['fitness']])




if __name__ == "__main__":
    main()
