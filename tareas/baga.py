"""
Base Binary Genetic Algorithm


Roulette-based selection
Random mutation
Optional elitism
"""
import random as rand
import math

class BaseGA:

    def __init__(self, init_pop = 2, max_cycles = 1, mut_rate = 0.001, opc = 1):

        self.opc = opc
        self.pop_size = init_pop

        # set max and min values
        if self.opc == 1:
            self.min = -5.1200
            self.max = 5.1200
            r = (self.max * 2) * 10000
            self.length = math.ceil(math.log2(r))
        elif self.opc == 2:
            self.min = -5.0000
            self.max = 5.0000
             r = (self.max * 2) * 10000
             self.length = math.ceil(math.log2(r)) * 2
        elif self.opc == 3:
            self.min = -512.0000
            self.max = 512.0000
            r = (self.max * 2) * 10000
            self.length = math.ceil(math.log2(r)) * 2
        
       

        self.max_cycles = max_cycles

        self.count = 0 # benchmark function calls

        self.population = [
            {
                'genes': 
                   [rand.randrange(0,1) for i in range(self.length)],
                'eval': 0.,
                'x': 0.,
                'y': 0.,
                'prob': 0.,
                'fitness': 0.
            } for x in range(init_pop)]
        
        self.children = []

        for ind in pop:
            decode(ind)

        self.eval_pop(self.population)


   
    def selection(self):

        """ 
        TODO: seleccion por ruleta
        """

        total_fitness = 0
        total_prob = 0
        for ind in self.population:
            total_fitness += ind['eval']

        for  ind in self.population:
            prob_ind = total_prob + (ind['eval'] / total_fitness)
            ind['prob'] = prob_ind
            total_prob += prob_ind
        
        self.taken = []

        while len(self.taken) < self.pop_size:
            r = rand.rand()
            for ind in self.population:
                if r <= ind['prob']:
                    taken.append(ind)
                    break
            
        
        # print(self.taken)
                
    def crossover(self):
        for i in range(len(self.population)):
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

            cross_point = rand.randrange(len(self.population[i]['genes']))

            for j in range(cross_point):
                first['genes'].append(self.population[i]['genes'][j])
                second['genes'].append(self.population[self.taken[i]]['genes'][j])
            for j in range(cross_point, len(self.population[i]['genes'])):
                first['genes'].append(self.population[self.taken[i]]['genes'][j])
                second['genes'].append(self.population[i]['genes'][j])

            self.children.append(first)
            self.second.append(first)

            # if self.opc == 1:
            #     first = self.rastrigin(first)
            #     second = self.rastrigin(second)
            # elif self.opc == 2:
            #     first = self.himmelblau(first)
            #     second = self.himmelblau(second)
            # elif self.opc == 3:
            #     first = self.eggholder(first)
            #     second = self.eggholder(second)

            # if first['eval'] < self.females[i]['eval']:
            #     self.females[i] = first
            
            # if second['eval'] < self.males[self.taken[i]]['eval']:
            #     self.males[self.taken[i]] = second
        

    def mutation(self):
        rate = 1 / self.length
        for i in range(len(self.children)):
            rand_gene = rand.randrange(len(self.children[i]['genes']))
            
            r = rand.rand()

            if r <= rate:
                self.children[i]['genes'][rand_gene] = 0 if self.children[i]['genes'][rand_gene] = 1 else  self.children[p]['genes'][rand_gene] = 1

            for ind in self.children:
                decode(ind)

            self.eval_pop(self.children)

            

    def eval_pop(self, population):
        for i in range(len(population)):
            if self.opc == 1:
                population[i] = self.rastrigin(self.population[i])
            elif self.opc == 2:
                population[i] = self.himmelblau(self.population[i])
            elif self.opc == 3:
                population[i] = self.eggholder(self.population[i])


    def rastrigin(self, individual):
        s = 0
        factor = 10 * len(individual['genes'])
        for i in individual['genes']:
            s += i ** 2 - 10 * math.cos(2 * math.pi * i)
        individual['eval'] = factor + s

        self.count += 1

        return individual
    
    def himmelblau(self, individual):
        individual['eval'] = (individual.x ** 2 + individual.y - 11) ** 2 + (individual.x + individual.y ** 2 - 7) ** 2

        return individual
    
    def eggholder(self, individual):

        individual['eval'] = (individual.y + 47) * math.sin(math.sqrt(abs((x / 2) + (individual.y + 47)))) - individual.x * math.sin(math.sqrt(abs(x - (y - 47))))

        return individual

    # def encode(self, number):
    #     genes = []
    #     if self.opc == 1:
    #        for i in range(self.length):
    #            genes[i]
    #     elif self.opc == 2:
    #         self.min = -5.0000
    #         self.max = 5.0000
    #     elif self.opc == 3:
    #         self.min = -512.0000
    #         self.max = 512.0000
       
    
    def decode(self, individual):
        s1 = ""
        s2 = ""
        if self.opc == 1:
            for gene in genes:
                s1 += str(gene)
            x = self.min + 0.0001 * int(s1, 2)
            individual['x'] = x
        else:
            for i in range(len(genes) / 2):
                s1 += str(genes[i])
            for i in range((len(genes) / 2), len(genes)):
                s2 += str(genes[i])
            x = self.min + 0.0001 * int(s1, 2)
            y = self.min + 0.0001 * int(s2, 2)
            individual['x'] = x
            individual['y'] = y
        
        return individual



        
def main():

    d = Daga(550, 500000, 0.005, 1)

    while(d.count <= d.max_cycles):
        d.selection()
        d.crossover()
        d.mutation()
    print(d.population)

if __name__ == "__main__":
    main()


