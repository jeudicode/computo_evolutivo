"""
Differential Evolution
"""
import test_functions as bench
import random as rand
import math
import csv

class DE:

    def __init__(self, pop_size = 2, dim = 1, max_cycles = 1, f = 0.5, cp = 0.9, opc = 1):
        rand.seed()

        self.best = []
        self.opc = opc
        self.pop_size = pop_size
        self.dim = dim
        self.f = f # scaling factor
        self.cp = cp # crossover probability
        self.max_cycles = max_cycles

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

        
        self.count = 0  # benchmark function calls

        self.population = [
          {
            'x': [round(rand.uniform(self.min, self.max), 6) for i in range(self.dim)],
            'eval': 0.,
          }  for x in range(self.pop_size)
        ]

        self.eval_pop(self.population)

        self.new_pop = []

        self.get_best()

        # print("****** INITIAL POPULATION ******")
        # for ind in self.population:
        #     print(str(ind['x']) + " " +  str(ind['eval']))
    
    def diff_evol(self):
        self.g = 0
        while self.g < self.max_cycles:
            for (i, ind) in enumerate (self.population):
                j = rand.randint(0, self.dim)
                k = rand.randint(0, self.dim)
                l = rand.randint(0, self.dim)
                n = rand.randint(0, self.dim)
                while j == i:
                    j = rand.randint(0, self.dim)
                while k == i:
                    k = rand.randint(0, self.dim)
                while l == i:
                    l = rand.randint(0, self.dim)
                while n == i:
                    n = rand.randint(0, self.dim)
                
                v = {
                    'x': [],
                    'eval': 0.,
                }

                for p in range(self.dim):
                    x = self.best[-1]['x'][p] + (self.f * (self.population[j]['x'][p] - self.population[k]['x'][p])) + (self.f * (self.population[l]['x'][p] - self.population[n]['x'][p]))

                    x = round(x, 6)

                    if x < self.min:
                       x = (2 * self.min) - x
                    if x > self.max:
                       x = (2 * self.max) - x
                    
                   

                    v['x'].append(x)


                # evaluate v
                self.eval(v)

                # print("v: ", str(v['x']))

                # mate current individual with v and get a child
                u = self.crossover(ind, v)

                # print("u: ", str(u['x']))

                if(u['eval'] <= ind['eval']):
                    self.new_pop.append(u)
                else:
                    self.new_pop.append(ind)

            self.population.clear()
            self.population = self.new_pop.copy()
            self.new_pop.clear()
            self.get_best()
            self.g += 1
    
    def crossover(self, x, v):
        u = {
            'x': [],
            'eval': 0.,
        }

        for i in range(self.dim):
            prob = rand.uniform(0, self.cp)
            r = rand.randint(0, self.dim)

            if prob <=self.cp or i == r:
                u['x'].append(v['x'][i])

            if prob > self.cp and i != r:
                u['x'].append(x['x'][i])


        self.eval(u)

        return u
    
    def getFitness(self, elem):
        return elem['eval']

    def get_best(self):
        best = self.population.copy()
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

    def eval(self, ind):
        if self.opc == 1:
            ind = bench.rastrigin(ind)
        elif self.opc == 2:
            ind = bench.himmelblau(ind)
        elif self.opc == 3:
            ind = bench.eggholder(ind)
        elif self.opc == 4:
            ind = bench.nqueens(ind)
        elif self.opc == 5:
            ind = bench.tsp(ind)
        
        self.count += 1
        
        return ind


def main():

   
    #p = DE(1000, 2, 300, 0.5, 0.75, 3)
    
    for i in range(10):
        p = DE(100, 2, 300, 0.2, 0.95, 3)
        p.diff_evol()

        # print("***** FINAL POPULATION *****")

        # for ind in p.best:
        #     print(str(ind['x']) + " " + str(ind['eval']))
        
    

        with open('res_de_today_'+str(p.opc)+'_' + str(i) + '_new.csv', mode='w') as res_file:
            res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            res_writer.writerow(['x','eval'])
            for ind in p.best:
                res_writer.writerow([ind['x'], ind['eval']])

if __name__ == "__main__":
    main()