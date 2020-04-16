import math
import random as rand
def rastrigin(individual):
    s = 0
    factor = 10 * 2
    for x in individual['x']:
        s += x ** 2 - 10 * math.cos(2 * math.pi * x)

    individual['eval'] = factor + s

    individual['eval'] = round(individual['eval'], 2)

    individual['fitness'] = 1 / (individual['eval'] + 0.001) 

    return individual

def himmelblau(individual):
    individual['eval'] = (individual['x'][0] ** 2 + individual['x'][1] -
                            11) ** 2 + (individual['x'][0] + individual['x'][1] ** 2 - 7) ** 2

    individual['eval'] = round(individual['eval'], 2)

    individual['fitness'] = 1 / (individual['eval'] + 0.001)
    
    return individual

def eggholder(individual):

    individual['eval'] = (individual['x'][1] + 47) * math.sin(math.sqrt(abs((individual['x'][0] / 2) + (
        individual['x'][1] + 47)))) - individual['x'][0] * math.sin(math.sqrt(abs(individual['x'][0] - (individual['x'][1] + 47))))

        
    #individual['fitness'] = -individual['eval']
    individual['eval'] = round(individual['eval'], 2)
    individual['fitness'] = -individual['eval']


    return individual


def tsp(individual):

    distances = [
        [0, 633, 257,  91, 412, 150,  80, 134, 259, 505, 353, 324,  70, 211, 268, 246, 121],
        [633, 0, 390, 661, 227, 488, 572, 530, 555, 289, 282, 638, 567, 466, 420, 745, 518],
        [257, 390, 0, 228, 169, 112, 196, 154, 372, 262, 110, 437, 191,  74,  53, 472, 142],
        [91, 661, 228,   0, 383, 120,  77, 105, 175, 476, 324, 240,  27, 182, 239, 237,  84],
        [412, 227, 169, 383,   0, 267, 351, 309, 338, 196,  61, 421, 346, 243, 199, 528, 297],
        [150, 488, 112, 120, 267,   0,  63,  34, 264, 360, 208, 329,  83, 105, 123, 364,  35],
        [80, 572, 196,  77, 351,  63,   0,  29, 232, 444, 292, 297,  47, 150, 207, 332,  29],
        [134, 530, 154, 105, 309,  34,  29,   0, 249, 402, 250, 314,  68, 108, 165, 349,  36],
        [259, 555, 372, 175, 338, 264, 232, 249,   0, 495, 352,  95, 189, 326, 383, 202, 236],
        [505, 289, 262, 476, 196, 360, 444, 402, 495,   0, 154, 578, 439, 336, 240, 685, 390],
        [353, 282, 110, 324,  61, 208, 292, 250, 352, 154,   0, 435, 287, 184, 140, 542, 238],
        [324, 638, 437, 240, 421, 329, 297, 314,  95, 578, 435,   0, 254, 391, 448, 157, 301],
        [70, 567, 191,  27, 346,  83,  47,  68, 189, 439, 287, 254,   0, 145, 202, 289,  55],
        [211, 466,  74, 182, 243, 105, 150, 108, 326, 336, 184, 391, 145,   0,  57, 426,  96],
        [268, 420,  53, 239, 199, 123, 207, 165, 383, 240, 140, 448, 202,  57,   0, 483, 153],
        [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157, 289, 426, 483,   0, 336],
        [121, 518, 142,  84, 297,  35,  29,  36, 236, 390, 238, 301,  55,  96, 153, 336,   0 ],
    ]

    sum = 0

    for i in range(1, len(individual['x'])):
        x = int(individual['x'][i-1])
        y = int(individual['x'][i])

        sum += distances[x][y]

    # closing the cycle
    x = int(individual['x'][0])
    y = int(individual['x'][-1])
    sum += distances[x][y]

    individual['eval'] = sum
    individual['fitness'] = 1/((sum-2085)+0.01)
    return individual


def nqueens(individual):
    collisions = 0

    for i in range(len(individual['x'])):
        for j in range(len(individual['x'])):
            if i != j:
                m = (int(individual['x'][j]) - int(individual['x'][i])) / (j - i)
                if abs(m) == 1 or abs(m) == 0:
                    collisions += 1
      
    
    individual['eval'] = collisions
    individual['fitness'] = 1 / (collisions + 0.01)
    return individual

def casp(ind, s):
    print(len(ind['coords']))
    non_local = 0
    ev = 0
    if ind['penalty'] > 0:
        ev = 0
        non_local = ind['penalty'] * -1
    else:
        for i in range(len(ind['coords']) - 1):
            for j in range(i + 1, len(ind['coords'])):
                d = math.sqrt((ind['coords'][j][0] - ind['coords'][i][0]) ** 2
                    + (ind['coords'][j][1] - ind['coords'][i][1]) ** 2)
                if d == 1:
                    if s[i] == "H" and s[j] == "H":
                        ev -= 1
                        if j - i > 1:
                            non_local += 1
    
    ind['eval'] = ev
    ind['fitness'] = non_local

    return ind
