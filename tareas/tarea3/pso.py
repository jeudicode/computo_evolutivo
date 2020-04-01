"""
Particle Swarm Optimization (PSO)
"""
import test_functions as bench
import random as rand
import math
import csv

class PSO:

    def __init__(self, pop_size = 2, dim = 1, max_cycles = 1, alpha = 0.5, c1 = 0.5, c2 = 0.5, opc = 1):
        rand.seed()

        self.best = []
        self.opc = opc
        self.pop_size = pop_size
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
            self.max = self.dim
        elif self.opc == 5:
            self.min = 0
            self.max = self.dim

        self.max_cycles = max_cycles
        self.count = 0  # benchmark function calls

        self.alpha = alpha # inertia
        self.c1 = c1 # rand.random()
        self.c2 = c2 # rand.random()

        self.population = [
          {
            'x': [round(rand.uniform(self.min, self.max), 6) for i in range(self.dim)],
            'v': [round(rand.random(), 6) for i in range(self.dim)],
            'eval': 0.,
          }  for x in range(self.pop_size)
        ]

        self.eval_pop(self.population)

        self.memory = self.population.copy() # best solution found by each particle

        self.get_best()

        # print("****** INITIAL POPULATION ******")
        # for ind in self.population:
        #     print(str(ind['x']) + " " +  str(ind['eval']))

        # print(str(self.best[-1]['x']) + " " + str(self.best[-1]['eval']))


    def pso(self):
        g = 0
        while(g < self.max_cycles):
            for (i, ind) in enumerate(self.population):
                for j in range(self.dim):
                    r1 = round(rand.random(), 2)
                    r2 = round(rand.random(), 2)

                    # update velocity of agent
                    ind['v'][j] = self.alpha * ind['v'][j] + (self.c1 * r1 * (self.memory[i]['x'][j] - ind['x'][j])) + (self.c2 * r2 * (self.best[-1]['x'][j] - ind['x'][j]))

                    ind['v'][j] = round(ind['v'][j], 2)

                    # update position
                    ind['x'][j] += ind['v'][j]
                    ind['x'][j] = round(ind['x'][j], 6)

                    if ind['x'][j] < self.min:
                       ind['x'][j] = (2 * self.min) -  ind['x'][j]
                    if ind['x'][j] > self.max:
                       ind['x'][j] = (2 * self.max) -  ind['x'][j]
        
            self.eval_pop(self.population)

            # update memory
            for (i, ind) in enumerate(self.population):
                if ind['eval'] <= self.memory[i]['eval']:
                    self.memory[i] = ind.copy()

            # update best
            self.get_best()

            g += 1


    def getFitness(self, elem):
        return elem['eval']

    def get_best(self):
        best = self.memory.copy()
        best.sort(key=self.getFitness)
        self.best.append(best[0])

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

    for i in range(10):
        p = PSO(100, 2, 300, 0.3, 0.4, 0.7, 3)
        p.pso()

        # print("***** FINAL POPULATION *****")

        # for ind in p.population:
        #     print(str(ind['x']) + " " + str(ind['eval']))
        
        with open('res_pso_today_'+str(p.opc)+'_' + str(i) + '_new.csv', mode='w') as res_file:
            res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            res_writer.writerow(['x','eval', 'fitness'])
            for ind in p.best:
                res_writer.writerow([ind['x'], ind['eval'], ind['fitness']])

if __name__ == "__main__":
    main()
