import random

demand = 5000

p = ((500, 2000), (100, 1500), (250, 1600), (250, 1600), (50, 1000))

n = 5
p_size = 100
ITER = 100


def population():
    pop = list()
    while True:
        tmp = list()
        for j in p:
            x = random.randint(j[0], j[1])
            tmp.append(x)
        if sigma(tmp) > demand:
            continue
        pop.append(tmp)
        if len(pop) >= 100:
            break
    return pop


def fitness(pop):
    cost = list()
    for i, value in enumerate(pop):
        tmp = cost_func(value)
        sig = sigma(tmp)
        cost.append([i, sig])
    cost.sort(key=lambda x: x[1])
    return cost


def selection(pop):
    mates = random.choices(pop, k=2)
    return mates


def crossover(mates):
    parent1 = mates[0]
    parent2 = mates[1]

    offspring1 = parent1.copy()
    offspring2 = parent2.copy()

    rnd = random.randint(1, 3)

    for i in range(rnd, n):
        gene1 = parent1[i]
        gene2 = parent2[i]
        b = random.random()

        gene1 = (gene1 - p[i][0]) / (p[i][1] - p[i][0])
        gene2 = (gene2 - p[i][0]) / (p[i][1] - p[i][0])

        new_gene_1 = b * gene1 + gene2 - b * gene2
        new_gene_2 = b * gene2 + gene1 - b * gene1

        new_gene_1 = (p[i][1] - p[i][0]) * new_gene_1 + p[i][0]
        new_gene_2 = (p[i][1] - p[i][0]) * new_gene_2 + p[i][0]

        new_gene_1 = int(new_gene_1)
        new_gene_2 = int(new_gene_2)

        offspring1[i] = new_gene_1
        offspring2[i] = new_gene_2
    if check_crossover_validation(offspring1) and check_crossover_validation(offspring2):
        return offspring1, offspring2
    elif check_crossover_validation(offspring1):
        return offspring1, None
    elif check_crossover_validation(offspring2):
        return offspring2, None
    else:
        return None, None


def check_crossover_validation(row):
    for i in range(n):
        if row[i] < p[i][0] and row[i] > p[i][1]:
            return False
    return True


def mutation():
    pass


def sigma(row):
    tmp = 0
    for i in row:
        tmp += i
    return tmp


def cost_func(p):
    p = (10 * p[0] ** 2 + 200 * p[0], 1000 * p[1] + 100, 1000 * p[2] + 100, p[3] ** 3 + 2 * p[3] ** 2,
         p[4] ** 3 + 2 * p[4] ** 2)
    return p


def sort_new_pop(pop, cost):
    new_pop = [0 for i in range(len(pop))]
    for i, value in enumerate(cost):
        new_pop[i] = pop[value[0]]
    return new_pop


def main():
    pop = population()
    cost = fitness(pop)
    pop = sort_new_pop(pop, cost)
    for i in range(ITER):
        for i in range(50):
            mates = selection(pop)
            offspring1, offspring2 = crossover(mates)
            if offspring1 is not None:
                pop.append(offspring1)
            if offspring2 is not None:
                pop.append(offspring2)
        cost = fitness(pop)
        pop = sort_new_pop(pop, cost)
        pop = pop[0:100]
    for i in pop:
        if sigma(i) > 1000:
            print(i)
            print(sigma(cost_func(i)))


if __name__ == '__main__':
    main()
