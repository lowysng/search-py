from map import romania, distance_bucharest
from sys import argv

INITIAL_CITY = 'Arad'
DESTINATION_CITY = 'Bucharest'
CUTOFF = 'cutoff'
FAILURE = 'failure'
INF = (2**31) - 1

class Problem:
	def __init__(self, states, initial_state, get_actions, transition_result, goal_test, step_cost):
		self.states = states
		self.initial_state = initial_state
		self.get_actions = get_actions
		self.transition_result = transition_result
		self.goal_test = goal_test
		self.step_cost = step_cost

problem = Problem(
	romania.cities,
	INITIAL_CITY,
	romania.get_connecting_cities,
	lambda from_city, to_city: to_city,
	lambda city: city == DESTINATION_CITY,
	lambda from_city, to_city: romania.step_cost(from_city, to_city))

class Node:
	def __init__(self, state, parent, action, path_cost):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost

def child_node(problem, parent, action):
	return Node(problem.transition_result(parent.state, action), parent, action, parent.path_cost + problem.step_cost(parent.state, action))

def solution(node, path_cost):
	if node.parent == None:
		return [path_cost, node.state]
	else:
		return solution(node.parent, path_cost) + [node.state]

def bfs(problem):
	"""Breadth-First Search"""
	node = Node(problem.initial_state, None, None, 0)
	if problem.goal_test(node.state):
		return solution(node, node.path_cost)
	frontier = [node]
	explored = []
	while len(frontier) != 0:
		node = frontier.pop(0)
		explored.append(node.state)
		for action in problem.get_actions(node.state):
			child = child_node(problem, node, action)
			if child.state not in explored and child.state not in frontier:
				if problem.goal_test(child.state):
					return solution(child, child.path_cost)
				frontier.append(child)
	return FAILURE

def ucs(problem):
	"""Uniform-Cost Search"""
	node = Node(problem.initial_state, None, None, 0)
	if problem.goal_test(node.state):
		return solution(node, node.path_cost)
	frontier = [node]
	explored = []
	while len(frontier) != 0:
		node = frontier.pop(0)
		if problem.goal_test(node.state):
			return solution(node, node.path_cost)
		explored.append(node.state)
		for action in problem.get_actions(node.state):
			child = child_node(problem, node, action)
			if child.state not in explored and child.state not in frontier:
				frontier.append(child)
				frontier.sort(key=lambda node: node.path_cost)
			elif child.state in frontier:
				index = frontier.index(child)
				if frontier[index].path_cost > child.path_cost:
					frontier[index] = child

def dfs(problem):
	"""Depth-first Search"""
	node = Node(problem.initial_state, None, None, 0)
	if problem.goal_test(node.state):
		return solution(node, node.path_cost)
	frontier = [node]
	explored = []
	while len(frontier) != 0:
		node = frontier.pop(0)
		explored.append(node.state)
		for action in problem.get_actions(node.state):
			child = child_node(problem, node, action)
			if child.state not in explored and child.state not in frontier:
				if problem.goal_test(child.state):
					return solution(child, child.path_cost)
				frontier = [child] + frontier
	return FAILURE


def dls(problem, limit):
	"""(Recursive) Depth-Limited Search"""
	def recursive_dls(node, problem, limit):
		if problem.goal_test(node.state):
			return solution(node, node.path_cost)
		elif limit == 0:
			return CUTOFF
		else:
			is_cutoff = False
			for action in problem.get_actions(node.state):
				child = child_node(problem, node, action)
				result = recursive_dls(child, problem, limit - 1)
				if result == CUTOFF:
					is_cutoff = True
				elif result != FAILURE:
					return result
			if is_cutoff:
				return CUTOFF
			else:
				return FAILURE

	return recursive_dls(Node(problem.initial_state, None, None, 0), problem, limit)

def ids(problem):
	"""Iterative Deepening Depth-Limited Search"""
	depth = 0
	while True:
		result = dls(problem, depth)
		if result != CUTOFF:
			return result
		depth += 1

def a_star(problem):
	"""Best First Search (A*)"""
	node = Node(problem.initial_state, None, None, 0)
	node.f = distance_bucharest(node.state)
	if problem.goal_test(node.state):
		return solution(node, node.f)
	frontier = [node]
	explored = []
	while len(frontier) != 0:
		node = frontier.pop(0)
		if problem.goal_test(node.state):
			return solution(node, node.f)
		explored.append(node.state)
		for action in problem.get_actions(node.state):
			child = child_node(problem, node, action)
			child.f = child.path_cost + distance_bucharest(child.state)
			if child.state not in explored and child.state not in frontier:
				frontier.append(child)
				frontier.sort(key=lambda node: node.f)
			elif child.state in frontier:
				index = frontier.index(child)
				if frontier[index].f > child.f:
					frontier[index] = child


def rbfs(problem):
	"""Recursive Best First Search"""
	def rbfs_(problem, node, f_limit):
		if problem.goal_test(node.state):
			return solution(node, node.path_cost), None
		successors = []
		for action in problem.get_actions(node.state):
			successors.append(child_node(problem, node, action))
		if len(successors) == 0:
			return FAILURE, INF
		for s in successors:
			s.f = max(s.path_cost + distance_bucharest(s.state), node.f)
		while True:
			successors.sort(key=lambda node: node.f)
			best = successors[0]
			if best.f > f_limit:
				return FAILURE, best.f
			alternative = successors[1].f
			result, best.f = rbfs_(problem, best, min(f_limit, alternative))
			if result != FAILURE:
				return result, None
	node = Node(problem.initial_state, None, None, 0)
	node.f = 0
	result, _ = rbfs_(problem, node, INF)
	return result

print("Breadth-first search:", bfs(problem))
print("Uniform-cost search:", ucs(problem))
print("Depth-first search:", dfs(problem))
print("Depth-limited search:", dls(problem, 3))
print("Iterative deepening depth-first search:", ids(problem))
print("A* search:", a_star(problem))
print("Recursive best first search:", rbfs(problem))