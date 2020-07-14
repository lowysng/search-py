# randomly-generated string --> user string
# Example: 'djfoefjwodm' --> 'hello world'

import random
from math import exp

alphabet = {
        26: 'a', 27: 'b',
        28: 'c', 29: 'd',
        30: 'e', 31: 'f',
        32: 'g', 33: 'h',
        34: 'i', 35: 'j',
        36: 'k', 37: 'l',
        38: 'm', 39: 'n',
        40: 'o', 41: 'p',
        42: 'q', 43: 'r',
        44: 's', 45: 't',
        46: 'u', 47: 'v',
        48: 'w', 49: 'x',
        50: 'y', 51: 'z',
        52: ' ', 53: '!',
        54: '.', 55: '-',

        }

MIN = list(alphabet.keys())[0]
MAX = list(alphabet.keys())[-1]

random.seed(42)

class Agent:

    def __init__(self):
        self.initial_state = []
        self.goal_state = []
        self.goal_state_encoding = []

    def initialise(self):
        random_string = random.choices(list(alphabet.values()), k=len(self.goal_state))
        self.initial_state = random_string
        return self.initial_state

    def set_goal(self, goal_state):
        self.goal_state = goal_state
        self.goal_state_encoding = [self.letter_to_int(s) for s in goal_state]
        return self.goal_state

    def get_successors(self, state):
        successors = []
        int_encoding = [self.letter_to_int(letter) for letter in self.initial_state]
        for i in range(len(int_encoding)):
            for j in range(26, 52):
                if int_encoding[i] != j:
                    successor = state.copy()
                    successor[i] = self.int_to_letter(j)
                    successors.append(successor)
        return successors

    def fitness(self, state):
        state_encoding = [self.letter_to_int(s) for s in state]
        fitness_score = 0
        for idx, e in enumerate(state_encoding):
            fitness_score += abs(self.goal_state_encoding[idx] - e)
        return fitness_score

    def letter_to_int(self, letter):
        return [i for i, l in alphabet.items() if l == letter][0]
    
    def int_to_letter(self, integer):
        return alphabet[integer]

def genetic_algorithm(population, fitness):
    num_letters = 25
    size_of_individual = len(population[0])
    step = 0
    step_limit = 500
    epsilon = 0.1

    def compute_weights(population):
        fitness_scores = [fitness(p) for p in population]
        softmax = [exp(num_letters * size_of_individual - f) for f in fitness_scores]
        weights = [s/sum(softmax) for s in softmax]
        return weights

    def reproduce(x, y):
        random_int = random.randint(0, len(x) - 1)
        return x[:random_int] + y[random_int:]

    def mutate(x):
        random_int = random.randint(0, len(x) - 1)
        x_copy = x.copy()
        x_copy[random_int] = alphabet[random.randint(MIN, MAX)]
        return x_copy

    population_history = [population]
    population_fitness = [fitness(p) for p in population]

    while 0 not in population_fitness and step < step_limit:
        if step % 1 == 0:
            print("Generation {} --> {} ({})".format(step, ''.join(population[0]), fitness(population[0])))
        new_population = []
        weights = compute_weights(population)
        for _ in range(len(population)):
            x = random.choices(population, weights=weights, k=1)[0]
            y = random.choices(population, weights=weights, k=1)[0]
            child = reproduce(x, y)
            random_float = random.uniform(0, 1)
            if random_float < epsilon:
                child = mutate(child)
            new_population.append(child)
        population = new_population
        population_history.append(population)
        population_fitness = [fitness(p) for p in population]
        step += 1

    population.sort(key=lambda s: fitness(s))
    print("Generation {} --> {} ({})".format(step, ''.join(population[0]), fitness(population[0])))
    return population[0], step, population_history

user = input("\n\nEnter word: ")

agent = Agent()
agent.set_goal(list(user))
agent.initialise()

successors = agent.get_successors(agent.initial_state)
print("Running genetic algorithm...")
solution, step_count, history = genetic_algorithm(successors, agent.fitness)
print("Solution found in generation {}: {}".format(step_count, ''.join(solution)))