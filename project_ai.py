import numpy as np
from project_state import *

def evaluator_1(DB):
	return DB.score

def evalutor_2(DB):
	return DB.score

def minimaxAB(DB, depth=5, a=-np.inf, b=np.inf, AI=0, evaluator=evaluator_1, node=False):
	if DB.lines_to_score() <= 1:
		return perform_action(DB, np.random.choice(DB.valid_actions())), 0

	if node:
		exec(node + ' = ' + node + ' + 1')

	if DB.end_game():
		return None, DB.score if AI == 0 else DB.score * (-1)
	if depth == 0:
		return None, evaluator(DB) if AI == 0 else evaluator(DB) * (-1)

	children = [perform_action(DB, n) for n in DB.valid_actions()]
	results = [minimaxAB(c, depth-1, a, b, AI=AI, evaluator=evaluator, node=node) for c in children]

	if DB.player == AI:
		v = -np.inf		
		for child, utility in results:
			v = max(v, utility)
			if v >= b:
				return child, v
			a = max(a, v)

	else:
		v = np.inf
		for child, utility in results:
			v = min(v, utility)
			if v <= a:
				return child, v
			b = min(b, v)

	_, utilities = zip(*results)
	utilities = np.array(utilities)
	if DB.player == AI: action = np.random.choice(np.where(utilities == max(utilities))[0])
	if DB.player == 1 - AI: action = np.random.choice(np.where(utilities == min(utilities))[0])
	return children[action], utilities[action]

if __name__ == "__main__":
	#a = Dots_Boxes(4)
	#b = minimaxAB(a, 4)
	#c, d = b
	#c.show()
	#a.show()
	#while(not a.end_game()):
	#	if a.player == 1:
	#		a, _ = minimaxAB(a, 3, AI=a.player)
	#	else:
	#		a = perform_action(a, np.random.choice(a.valid_actions()))
	#	a.show()
	import pandas as pd

	nodes = np.array([[1] * 100] * 5)
	net_s = np.array([[0] * 100] * 5)

	for i in [2, 3, 4, 5, 6]:
		for j in range(100):
			a = Dots_Boxes(i)
			while not a.end_game():
				if a.player == j % 2:
					action = np.random.choice(a.valid_actions())
					a = perform_action(a, action)
				else:
					a, _ = minimaxAB(a, 3, AI=a.player, node='nodes[i-2, j]')
			#nodes[i-2, j] = node
			net_s[i-2, j] = a.score * pow(-1, j % 2 + 1)

	nd = pd.DataFrame(nodes)
	ns = pd.DataFrame(net_s)

	writer = pd.ExcelWriter('simulation.xlsx')
	nd.to_excel(writer, 'NODES')
	ns.to_excel(writer, 'SCORES')

	writer.save()
	writer.close()

