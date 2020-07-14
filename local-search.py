from EightQueens import EightQueens 
import random
from math import exp, floor

class Node:
    def __init__(self, state, value):
        self.state = state
        self.value = value

def hill_climbing(eight_queens):
    initial_state = eight_queens.initial_state
    initial_value = eight_queens.heuristic(initial_state)
    current = Node(initial_state, initial_value)
    history = [initial_state]

    step_limit = 100
    step_count = 0
    step_value = 0

    while True:
        successors = eight_queens.get_successors(current.state)
        random.shuffle(successors)
        successors.sort(key=lambda s: eight_queens.heuristic(s))
        best_successor = Node(successors[0], eight_queens.heuristic(successors[0]))

        if best_successor.value > current.value:
            return current.state, history
        elif best_successor.value == current.value:
            if step_count < step_limit:
                if best_successor.value != step_value:
                    step_count = 0
                    step_value = best_successor.value
                else:
                    step_count += 1
            else:
                return current.state, history
        current = best_successor
        history.append(current.state)

def simulated_annealing(eight_queens, schedule):
    initial_state = eight_queens.initial_state
    initial_value = eight_queens.heuristic(initial_state)
    current = Node(initial_state, initial_value)
    history = [initial_state]

    t = 0

    while True:
        if (t > 5):
            t = 5
        T = schedule(t)
        if T == 0:
            return current.state, history
        successors = eight_queens.get_successors(current.state)
        random.shuffle(successors)
        successor_state = successors[0]
        successor_value = eight_queens.heuristic(successor_state)
        successor = Node(successor_state, successor_value)
        delta_value = initial_value - successor_value
        if delta_value > 0:
            current = successor
        else:
            random_float = random.uniform(0, 1)
            if random_float < exp(delta_value/T):
                current = successor
        history.append(current.state)
        t += 0.001

def genetic_algorithm(eight_queens):
    population = eight_queens.get_successors(eight_queens.initial_state)
    population_fitness = [eight_queens.heuristic(state) for state in population]
    step_limit = 1000
    epsilon = 0.05

    def get_weights(population):
        fitness = [eight_queens.heuristic(state) for state in population]
        softmax = [exp(28 - f) for f in fitness]
        weights = [s/sum(softmax) for s in softmax]
        return weights

    def reproduce(x, y):
        random_int = random.randint(0, len(x) - 1)
        return x[:random_int] + y[random_int:]

    def mutate(x):
        random_int = random.randint(0, len(x) - 1)
        x_copy = x.copy()
        x_copy[random_int] = random.randint(0, 7)
        return x_copy

    step = 0

    while 0 not in population_fitness and step < step_limit:
        if step % 100 == 0:
            print("Generation {}".format(step))
        new_population = []
        weights = get_weights(population)
        for _ in range(len(population)):
            x = random.choices(population, weights=weights, k=1)[0]
            y = random.choices(population, weights=weights, k=1)[0]
            child = reproduce(x, y)
            random_float = random.uniform(0, 1)
            if random_float < epsilon:
                child = mutate(child)
            new_population.append(child)
        population = new_population
        population_fitness = [eight_queens.heuristic(state) for state in population]
        step += 1

    population.sort(key=lambda s: eight_queens.heuristic(s))
    return population[0], step


eight_queens = EightQueens()
eight_queens.init()
print("Starting heuristic cost: {}".format(eight_queens.heuristic(eight_queens.initial_state)))
print(eight_queens.stringify_state(eight_queens.initial_state))

print("Running hill climbing...")
hc_solution, hc_state_history = hill_climbing(eight_queens)
print("Num of steps taken to generate solution using Hill Climbing: {}".format(len(hc_state_history)))
print("Solution heuristic cost: {}\n".format(eight_queens.heuristic(hc_solution)))

print("Running simulated annealing...")
sa_solution, sa_state_history = simulated_annealing(eight_queens, lambda t : (t - 5) ** 2)
print("Num of steps taken to generate solution using Simulated Annealing: {} (constant)".format(len(sa_state_history)))
print("Solution heuristic cost: {}\n".format(eight_queens.heuristic(sa_solution)))

print("Running genetic algorithm...")
ga_solution, ga_step_count = genetic_algorithm(eight_queens)
print("Num of steps taken to generate solution using Genetic Algorithm: {}".format(ga_step_count))
print("Solution heuristic cost: {}\n".format(eight_queens.heuristic(ga_solution)))