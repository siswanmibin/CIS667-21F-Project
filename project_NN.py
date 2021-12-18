import numpy as np
import torch as tr
import pandas as pd
import matplotlib.pyplot as plt

from project_state import *
from project_ai import *

def to_array(df):
	sps = []
	for n in range(df.shape[0]):
		sps.append(np.array(df.iloc[n][1:]))
	return np.array(sps)

def utility(arr, SIZE=5):# Use mode if its frequency >= 60% else mean. Count: 59 modes, 66 means.
	ms = (SIZE - 1) ** 2
	ut = [np.argmax(np.bincount(s)) / ms if max(np.bincount(s)) >= 0.6 * len(s) else s.mean() / ms for s in arr]
	return np.array(ut).astype(np.float32)

def to_data(eva_file, samp_file):# Samples and Utilities	
	df1 = pd.read_excel(eva_file, engine='openpyxl')
	df2 = pd.read_excel(samp_file, engine='openpyxl')

	Simulations = to_array(df1)
	uti = utility(Simulations)
	uti = np.append(uti, uti, axis=0)
	Utilities = np.append(uti, uti, axis=0)
	Utilities = np.append(Utilities, uti, axis=0)
	Utilities = np.append(Utilities, uti, axis=0)
	Samples = to_array(df2)

	return Samples, Utilities

def batches(Samples, Utilities, seed=0):# Training and Testing Data
	np.random.seed(seed)
	N = len(Samples)
	order = np.random.permutation(N)
	train_serial = order[:N//2]
	test_serial = order[N//2:]
	
	training_batch = tr.stack(tuple(map(tr.tensor, Samples[train_serial]))), tr.tensor(Utilities[train_serial])
	testing_batch = tr.stack(tuple(map(tr.tensor, Samples[test_serial]))), tr.tensor(Utilities[test_serial])

	return training_batch, testing_batch

class Net1(tr.nn.Module): # One hidden layer. Use sigmod as activation function.
	def __init__(self, hid=10, size=5):
		super(Net1, self).__init__()
		self.to_hidden = tr.nn.Linear(size * (size - 1) * 2, hid)
		self.to_output = tr.nn.Linear(hid, 1)

	def forward(self, x):
	    h = self.to_hidden(x)
	    y = tr.sigmoid(self.to_output(h))
	    return y

def batch_error(net, batch):
	st, ut = batch
	u = ut.reshape(-1, 1).float()
	s = st.float()
	y = net(s)
	e = tr.sum((y-u)**2) / ut.shape[0]
	return e

if __name__ == "__main__":
	Samples, Utilities = to_data('evaluate.xlsx', 'samples.xlsx')
	training_batch, testing_batch = batches(Samples, Utilities)

	net = Net1()
	optimizer = tr.optim.SGD(net.parameters(), lr=0.005)

	curves = [], []
	for i in range(10000):
		optimizer.zero_grad()

		e = batch_error(net, training_batch)
		e.backward()
		tre = e.item()

		with tr.no_grad():
			e = batch_error(net, testing_batch)
			tee = e.item()

		optimizer.step()

		if i % 1000 == 0:
			print(f'{i}: {tre}, {tee}')

		curves[0].append(tre)
		curves[1].append(tee)

	ble = sum([(u - 0.5) ** 2 for u in Utilities]) / 1120
	plt.plot(curves[0], 'b-')
	plt.plot(curves[1], 'r-')
	plt.plot([0, len(curves[1])], [ble, ble], 'g-')
	plt.plot()
	plt.legend(["Train", "Test", "Baseline"])
	plt.savefig('Errors.png', bbox_inches='tight', dpi=800)

	def evaluator_nn(DB):
	    ipt = tr.tensor(DB.lines).float()
	    eva = net(ipt).data[0]
	    coef = 1 if DB.player == 0 else -1
	    return  float(eva * 16 * 2 - 16) * coef

	net_s = []
	for j in range(100):
		a = Dots_Boxes(5)
		while not a.end_game():
			if a.player == j % 2:
				action = np.random.choice(baseai(a))
				a = perform_action(a, action)
			else:
				a, _ = minimaxAB(a, 3, AI=a.player, evaluator=evaluator_nn)
		net_s.append(a.score * pow(-1, j % 2 + 1))

	nets = pd.DataFrame(net_s)
	writer = pd.ExcelWriter('nn_simulation.xlsx')
	nets.to_excel(writer, '1')
	writer.save()
	writer.close()

	net_s2 = []
	for j in range(100):
	    a = Dots_Boxes(5)
	    while not a.end_game():
	        if a.player == j % 2:
	            action = np.random.choice(baseai(a))
	            a = perform_action(a, action)
	        else:
	            a, _ = minimaxAB(a, 3, AI=a.player)
	    net_s2.append(a.score * pow(-1, j % 2 + 1))

	nets2 = pd.DataFrame(net_s2)
	writer = pd.ExcelWriter('new_simulation.xlsx')
	nets2.to_excel(writer, '1')
	writer.save()
	writer.close()
