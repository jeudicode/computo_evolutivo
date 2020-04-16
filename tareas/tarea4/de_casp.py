"""
Differential Evolution
"""
import test_functions as bench
import random as rand
import math
import csv

class DE:

    def __init__(self, pop_size = 2, max_cycles = 1, f = 0.5, cp = 0.9, string="", a=1, b=2, c=3, d=4, e=5):
        rand.seed()
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.string = string
        self.best = []
        self.pop_size = pop_size 
        self.dim = len(string) - 1
        self.f = f # scaling factor
        self.cp = cp # crossover probability
        self.max_cycles = max_cycles   
        self.count = 0  # benchmark function calls

        self.population = [
          {
            'x': [rand.uniform(self.d, self.e) for i in range(len(string) - 1)],
            'movements': [],
            'coords': [[0,0]],
            'eval': 0.,
            'fitness': 0,
            'penalty': 0
          }  for x in range(self.pop_size)
        ]

        for ind in self.population:
            ind = self.get_movements(ind)
            ind = self.get_coords(ind)

        self.eval_pop(self.population)

        self.new_pop = []

        self.get_best()

        print("****** INITIAL POPULATION ******")
        for ind in self.population:
            print(str(ind['movements']) + " " +  str(ind['fitness']))
    
    def diff_evol(self):
        self.g = 0
        while self.g < self.max_cycles:
            for (i, ind) in enumerate (self.population):
                j = rand.randint(0, self.pop_size - 1)
                k = rand.randint(0, self.pop_size - 1)
                l = rand.randint(0, self.pop_size - 1)
                n = rand.randint(0, self.pop_size - 1)
                while j == i:
                    j = rand.randint(0, self.pop_size - 1)
                while k == i:
                    k = rand.randint(0, self.pop_size - 1)
                while l == i:
                    l = rand.randint(0, self.pop_size - 1)
                while n == i:
                    n = rand.randint(0, self.pop_size - 1)
                
                # auxiliary mate
                v = {
                    'x': [],
                    'movements': [],
                    'coords': [[0,0]],
                    'eval': 0.,
                    'fitness': 0,
                    'penalty': 0
                }

                for p in range(self.dim):
                    x = self.best[-1]['x'][p] + (self.f * (self.population[j]['x'][p] - self.population[k]['x'][p])) + (self.f * (self.population[l]['x'][p] - self.population[n]['x'][p]))

                    x = round(x, 3)
                    

                    if x < self.a:
                       x = rand.uniform(self.a, self.b)
                    if x > self.e:
                       x = rand.uniform(self.d, self.e)

                    v['x'].append(x)
                
                v = self.get_movements(v)
                v = self.get_coords(v)
                v = self.eval(v)
                
                #print("v:", v['movements'])

                # mate current individual with v and get a child
                u = self.crossover(ind, v)

                #print("u:", u['movements'])


                if(u['fitness'] >= ind['fitness']):
                    self.new_pop.append(u)
                else:
                    self.new_pop.append(ind)

            self.population.clear()
            self.population = self.new_pop.copy()
            self.new_pop.clear()
            self.get_best()
            # print("****** POPULATION IN G = "  + str(self.g) + " ******")
            # for ind in self.population:
            #     print(str(ind['movements']) + " " +  str(ind['fitness']))
            self.g += 1
            self.f = (self.f * self.pop_size) / self.g
    
    def crossover(self, x, v):
        u = {
            'x': [],
            'movements': [],
            'coords': [[0,0]],
            'eval': 0.,
            'fitness': 0,
            'penalty': 0
        }

        for i in range(self.dim):
            prob = rand.uniform(0, self.cp)
            r = rand.randint(0, self.dim)

            if prob <= self.cp or i == r:
                u['x'].append(v['x'][i])

            if prob > self.cp and i != r:
                u['x'].append(x['x'][i])
        
        u = self.get_movements(u)
        u = self.get_coords(u)
        u = self.eval(u)

        return u
    
    def getFitness(self, elem):
        return elem['fitness']

    def get_best(self):
        best = self.population.copy()
        best.sort(key=self.getFitness, reverse=True)
        self.best.append(best[0])

    def eval_pop(self, population):
        for i in range(len(population)):
            population[i] = bench.casp(population[i], self.string)
            self.count += 1
        
        return population

    def eval(self, ind):
        ind = bench.casp(ind, self.string)
        self.count += 1
        
        return ind
    
    def get_movements(self, ind):
        for x in ind['x']:
            if x > self.a and x <= self.b:
                ind['movements'].append("F")
            elif x > self.b and x <= self.c:
                ind['movements'].append("B")
            elif x > self.c and x <= self.d:
                ind['movements'].append("L")
            elif x > self.d and x <= self.e:
                ind['movements'].append("R")
        
        for i in range(len(ind['movements']) - 1):
            if ind['movements'][i] == "F":
               if ind['movements'][i+1] == "B":
                   ind['penalty'] += 10
            elif ind['movements'][i] == "B":
               if ind['movements'][i+1] == "F":
                   ind['penalty'] += 10
            elif ind['movements'][i] == "L":
               if ind['movements'][i+1] == "R":
                   ind['penalty'] += 10
            elif ind['movements'][i] == "R":
               if ind['movements'][i+1] == "L":
                   ind['penalty'] += 10
        
        return ind

    def get_coords(self, ind):
        for i in range(len(ind['movements'])):
            if ind['movements'][i] == "F":
                c = [
                    ind['coords'][-1][0],
                    ind['coords'][-1][1] + 1
                ]

                if c in ind['coords']:
                    ind['penalty'] += 100

                ind['coords'].append(c)
            elif ind['movements'][i] == "B":
                c = [
                    ind['coords'][-1][0],
                    ind['coords'][-1][1] - 1
                ]

                if c in ind['coords']:
                    ind['penalty'] += 100

                ind['coords'].append(c)
            elif ind['movements'][i] == "L":
                c = [
                    ind['coords'][-1][0] - 1,
                    ind['coords'][-1][1] 
                ]

                if c in ind['coords']:
                    ind['penalty'] += 100

                ind['coords'].append(c)
            elif ind['movements'][i] == "R":
                c = [
                    ind['coords'][-1][0] + 1,
                    ind['coords'][-1][1] 
                ]

                if c in ind['coords']:
                    ind['penalty'] += 100

                ind['coords'].append(c)
        
        return ind


def main():
    #s = "HPHPPHHPHHPHPHHPPHPH"
    #s = "HHPPHPPHPPHPPHPPHPPHPPHH"    
    #s = "PPHPPHHPPPPHHPPPPHHPPPPHH"
    #s = "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP"
    s = "PPHPPHHPPHHPPPPPHHHHHHHHHHPPPPPP"
    p = DE(30, 500, 0.8, 0.9, s, -3, -1, 1, 3, 5)
    p.diff_evol()

    print("***** FINAL POPULATION *****")

    for ind in p.best:
        print(str(ind['movements']) + " " + str(ind['fitness']))

    # for i in range(10):
    #     p = DE(20, 500, 0.8, 0.9, s, 1, 2, 3, 4, 5)
    #     p.diff_evol()

    #     print("***** FINAL POPULATION *****")

    #     for ind in p.best:
    #         print(str(ind['x']) + " " + str(ind['eval']))
        
        # with open('res_de_today_'+str(p.opc)+'_' + str(i) + '_new.csv', mode='w') as res_file:
        #     res_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        #     res_writer.writerow(['x','eval'])
        #     for ind in p.best:
        #         res_writer.writerow([ind['x'], ind['eval']])

if __name__ == "__main__":
    main()