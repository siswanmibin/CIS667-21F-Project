import numpy as np
from project_state import *
from project_NN import *
import torch as tr

def evaluator_1(DB):
	sa = DB.score_aeras()
	ps = 0
	for i, j in sa:
		if sum(j) == 3:
			ps += 1
	return DB.score - ps if DB.player else DB.score + ps

def baseai(DB, com=True):
	if DB.lines_to_score() <= 1:
		return DB.valid_actions()
	sa = DB.score_aeras()
	vas = DB.valid_actions()
	Pas = set()
	pas = set()
	neg = set()
	for i, j in sa:
		if sum(j) == 3:
			Pas = Pas | set(i)
		elif sum(j) == 2:
			neg = neg | set(i)
		elif sum(j) <= 1:
			pas = pas | set(i)
	pas = pas - neg
	if com:
		if len(Pas & set(vas)) > 0:
			return list(Pas & set(vas))
		elif len(pas & set(vas)) > 0:
			return list(pas & set(vas))
		return vas
	else:
		if len(pas & set(vas)) > 0:
			return list(pas & set(vas))
		return vas

def minimaxAB(DB, depth=4, a=-np.inf, b=np.inf, AI=0, evaluator=evaluator_1, node=False):
	if DB.end_game():
		return None, DB.score * (-1) ** AI

	if node:
		exec(node + ' = ' + node + ' + 1')

	if DB.lines_to_score() <= 1:
		return perform_action(DB, np.random.choice(DB.valid_actions())), 0
		
	if depth == 0:
		return None, evaluator(DB) * (-1) ** AI

	children = [perform_action(DB, n) for n in baseai(DB)]
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
	import pandas as pd

	Samples, Utilities = to_data('evaluate.xlsx', 'samples.xlsx')
	training_batch, testing_batch = batches(Samples, Utilities)

	net = Net1()
	optimizer = tr.optim.SGD(net.parameters(), lr=0.005)

	for i in range(10000):
		optimizer.zero_grad()

		e = batch_error(net, training_batch)
		e.backward()
		tre = e.item()

		with tr.no_grad():
			e = batch_error(net, testing_batch)
			tee = e.item()

		optimizer.step()

	def evaluator_nn(DB):
	    ipt = tr.tensor(DB.lines).float()
	    eva = net(ipt).data[0]
	    coef = 1 if DB.player == 0 else -1
	    return  float(eva * 16 * 2 - 16) * coef

	nodes = np.array([[1] * 100] * 5)
	net_s = np.array([[0] * 100] * 5)

	for j in range(100):
		a = Dots_Boxes(5)
		while not a.end_game():
			if a.player == j % 2:
				action = np.random.choice(baseai(a))
				a = perform_action(a, action)
			else:
				a, _ = minimaxAB(a, 3, AI=a.player, evaluator=evaluator_nn, node='nodes[3, j]')
			net_s[3, j] = a.score * pow(-1, j % 2 + 1)

	nd = pd.DataFrame(nodes)
	ns = pd.DataFrame(net_s)

	writer = pd.ExcelWriter('simulation.xlsx')
	nd.to_excel(writer, 'NODES')
	ns.to_excel(writer, 'SCORES')

	writer.save()
	writer.close()
'''
	for i in [2, 3, 4, 5, 6]:
		md = 3 if i >= 5 else 4
		for j in range(100):
			a = Dots_Boxes(i)
			while not a.end_game():
				if a.player == j % 2:
					action = np.random.choice(baseai(a))
					a = perform_action(a, action)
				else:
					a, _ = minimaxAB(a, md, AI=a.player, node='nodes[i-2, j]')
			net_s[i-2, j] = a.score * pow(-1, j % 2 + 1)

	nd = pd.DataFrame(nodes)
	ns = pd.DataFrame(net_s)

	writer = pd.ExcelWriter('simulation.xlsx')
	nd.to_excel(writer, 'NODES')
	ns.to_excel(writer, 'SCORES')

	writer.save()
	writer.close()

'''