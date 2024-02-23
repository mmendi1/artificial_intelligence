import random
from itertools import permutations,combinations
import math
import statistics
import copy
import numpy as np
random.seed(1234)

#Generating 7 randoms cities
def generate_r7c():
    seven_cities = [None]*7
    for j in range(7):
        seven_cities[j] = [random.uniform(0, 1),random.uniform(0, 1)]
    return seven_cities

#Generating 100 instances of 7 cities each
instances = [None]*100
for i in range(100):
    instances[i] = generate_r7c()

#Compute distances for 7 cities
def distance_seven_cities(cities):
    distance = 0
    for i in range(len(cities)-1):
        distance += math.hypot(cities[i+1][0]-cities[i][0],cities[i+1][1]-cities[i][1])
    distance += math.hypot(cities[6][0]-cities[0][0],cities[6][1]-cities[0][1]) 
    return distance

#Compute distances for 100 cities
def distance_hundred_cities(muchas):
    distance = 0
    for i in range(len(muchas)-1):
        distance += math.hypot(muchas[i+1][0]-muchas[i][0],muchas[i+1][1]-muchas[i][1])
    distance += math.hypot(muchas[99][0]-muchas[0][0],muchas[99][1]-muchas[0][1])
    return distance

##############################################
# PART A - Solve each instance by brute force
#  ie. considering all possible permutations
##############################################

def permut_aslist(lista):
    a = [0]*len(lista)
    for i in range(len(lista)):
        a[i] = lista[i]
    return a
permut = []
for i in range(100):
    a = list(permutations(instances[i]))
    b = permut_aslist(a)
    permut.append(b)

#min for each instance
def get_min_of_one_instance(parametro):
    dist = []
    for i in range(len(parametro)):
        dist.append(distance_seven_cities(parametro[i]))
    result = np.min(dist)
    return result
mymatrix = []
for x in range(len(permut)):
    mymatrix.append(get_min_of_one_instance(permut[x]))

#These would be the statistics for A
a_mean = np.mean(mymatrix)
a_std = np.std(mymatrix)
a_min = np.min(mymatrix)
a_max = np.max(mymatrix)
print()
print("Results found using brute-force search: ")
print("Mean: " + str(a_mean))
print("Standard deviation " + str(a_std))
print("Minimum: " + str(a_min))
print("Maximum: " + str(a_max))
print()

####################################################
# Part B - Random tour of each of the 100 instances#
####################################################

random_instance = [None]*100
dist_instances = [0]*100
count = 0
for i in range(100):
    random.shuffle(permut[i])
    random_instance[i] = permut[i][0]
    dist_instances[i] = distance_seven_cities(random_instance[i])
    if (dist_instances[i] == mymatrix[i]):
        count += 1
min_rt = [None]*100
for i in range(100):
    min_rt[i] = np.min(dist_instances[i])

#These would be the statistics for B
b_mean = np.mean(min_rt)
b_std = np.std(min_rt)
b_min = np.min(min_rt)
b_max = np.max(min_rt)

print()
print("Results found a random permutation: ")
print("Mean: " + str(b_mean))
print("Standard deviation: " + str(b_std))
print("Minimum: " + str(b_min))
print("Maximum: " + str(b_max))
print("Number of instances for which the random tour happens to be the optimal solution: " + str(count))
print()

###################################
# Part C - Hill climbing algorithm#
###################################
def adjacent(x,y):
    if x+1==y:
        return False
    if x+1==y-1:
        return False

def new_tour_generator(tour,twoOpt):
    x,y = tour.index(twoOpt[0]), tour.index(twoOpt[1])
    new = list(copy.deepcopy(tour))
    possible = True
    while possible:
        if adjacent(x,y) == False:
            possible = False
        new[x],new[y] = new[y],new[x]
        x,y = x+1,y-1
    return new

def neighbourhood(current):
    neighbours = []
    pairs = list(combinations(current,2))
    for p in pairs:
        new = new_tour_generator(current,p)
        if distance_seven_cities(new)<distance_seven_cities(current):
            neighbours.append(new)
    return neighbours

def hill_climbing(cities):
    current = cities
    isBetter = True
    while isBetter:
        if len(neighbourhood(current))==0:
            isBetter = False
        for nei in neighbourhood(current):
            current = nei
    return distance_seven_cities(current)


def neighbourhood100(current):
    neighbours = []
    pairs = list(combinations(current,2))
    for p in pairs:
        new = new_tour_generator(current,p)
        if distance_hundred_cities(new)<distance_hundred_cities(current):
            neighbours.append(new)
    return neighbours

def hill_climbing100(cities):
    current = cities
    isBetter = True
    while isBetter:
        if len(neighbourhood100(current))==0:
            isBetter = False
        for nei in neighbourhood100(current):
            current = nei
    return distance_hundred_cities(current)

distances_hc = [0]*100
counter = 0
for i in range(len(random_instance)):
    distances_hc[i] = hill_climbing(random_instance[i])
    if (distances_hc[i] == mymatrix[i]):
        counter += 1

min_hc = [None]*100
for i in range(100):
    min_hc[i] = np.min(distances_hc[i])

#These would be the statistics for C
c_mean = np.mean(min_hc)
c_std = np.std(min_hc)
c_min = np.min(min_hc)
c_max = np.max(min_hc)

print()
print("Results found using Hill Climbing with the 2opt: ")
print("Mean: " + str(c_mean))
print("Standard deviation: " + str(c_std))
print("Minimum: " + str(c_min))
print("Maximum: " + str(c_max))
print("Number of instances for which the random tour happens to be the optimal solution: " + str(counter))
print()

#########
# Part D# 
#########

#Generate 100 cities
def generate_r100c():
    hundred_cities = [None]*100
    for j in range(100):
        hundred_cities[j] = [random.uniform(0, 1),random.uniform(0, 1)]
    return hundred_cities
alot = [None]*100
for i in range(100):
    alot[i] = generate_r100c()

# Random tours:
hundred_random = [0]*100
num = 0
for i in range(100):
    hundred_random[i] = distance_hundred_cities(alot[i])

min_hrt = [None]*100
for i in range(100):
    min_hrt[i] = np.min(hundred_random[i])

#These would be the statistics for D
d1_mean = np.mean(min_hrt)
d1_std = np.std(min_hrt)
d1_min = np.min(min_hrt)
d1_max = np.max(min_hrt)

print()
print("Results found a random permutation: ")
print("Mean: " + str(d1_mean))
print("Standard deviation: " + str(d1_std))
print("Minimum: " + str(d1_min))
print("Maximum: " + str(d1_max))
print()

distances_hill100 = [0]*100
#Using Hill Climbing:
for i in range(len(alot)):
    distances_hill100[i] = hill_climbing100(alot[i])

min_hhc = [None]*100
for i in range(100):
    min_hhc[i] = np.min(distances_hill100[i])

#These would be the statistics for D
d2_mean = np.mean(min_hhc)
d2_std = np.std(min_hhc)
d2_min = np.min(min_hhc)
d2_max = np.max(min_hhc)

print()
print("Results found a random permutation: ")
print("Mean: " + str(d2_mean))
print("Standard deviation: " + str(d2_std))
print("Minimum: " + str(d2_min))
print("Maximum: " + str(d2_max))
print()

   