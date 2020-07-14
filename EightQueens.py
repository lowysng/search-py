import random
from math import exp

class EightQueens:
    def __init__(self):
        self.initial_state = [random.randint(0, 7) for _ in range(8)]

    def init(self):
        self.initial_state = [random.randint(0, 7) for _ in range(8)]

    def get_successors(self, state):
        successors = []
        for col, row in enumerate(state):
            for new_row in range(8):
                if row != new_row:
                    s = state.copy()
                    s[col] = new_row
                    successors.append(s)
        return successors

    def heuristic(self, state):
        numPairsAttackingQueens = 0
        explored = []
        for col, row in enumerate(state):
            q_one = [col, row]  # queen_one = [x-coord, y-coord]
            for other_col in range(8):
                if col != other_col:
                    q_two = [other_col, state[other_col]]  # queen_two = [x-coord, y-coord]
                    if (self.queens_are_attacking(q_one, q_two)):
                        if (not self.in_explored_set(q_one, q_two, explored)):
                            explored.append(self.compose(q_one, q_two))
                            numPairsAttackingQueens += 1

        return numPairsAttackingQueens

    def queens_are_attacking(self, queen_one, queen_two):
        areAttacking = False
        if (queen_one[1] == queen_two[1]): # same row
            areAttacking = True
        else:
            def get_complements(num):
                start = num * -1
                end = start + 8
                complements = list(range(start, end))
                complements.remove(0)
                return complements
            def elem_wise_and(list_a, list_b):
                intersecting_elements = []
                for a_ in list_a:
                    if a_ in list_b:
                        intersecting_elements.append(a_)
                return intersecting_elements
            
            col_complements = get_complements(queen_one[0])
            row_complements = get_complements(queen_one[1])
            common_complements = elem_wise_and(col_complements, row_complements)

            for complement in common_complements:
                if ((queen_one[0] + complement == queen_two[0]) and (queen_one[1] + complement == queen_two[1])): # same main diagonal
                    areAttacking = True
            for col_complement in col_complements:
                if ((queen_one[0] + col_complement == queen_two[0]) and (queen_one[1] - col_complement == queen_two[1])): # same anti-diagonal
                    areAttacking = True

        return areAttacking
    
    def in_explored_set(self, queen_one, queen_two, explored):
        composed = self.compose(queen_two, queen_one)
        if composed in explored:
            return True
        else:
            return False

    def compose(self, queen_one, queen_two):
        return "{}{}{}{}".format(queen_one[0], queen_one[1], queen_two[0], queen_two[1])
    
    def parse(self, string):
        return [int(string[0]), int(string[1])], [int(string[2]), int(string[3])]

    def stringify_state(self, state):
        matrix = []
        for _ in range(8):
            matrix.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'])
        for c, r in enumerate(state):
            matrix[r][c+1] = 'X'
        return ''.join('|'.join(row) for row in matrix)



eq = EightQueens()
population = eq.get_successors(eq.initial_state)
fitness = [eq.heuristic(s) for s in population]
softmax = [exp(28 - f) for f in fitness]
probs = [s/sum(softmax) for s in softmax]
print(random.choices(population, weights=probs, k=1))