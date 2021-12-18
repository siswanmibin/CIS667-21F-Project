import numpy as np
from project_state import *
from project_ai import *

def samples(S, N, seed=1):# Samples for begin-to-score states, in which any action would result in scores of self or opponent.
	np.random.seed(seed)
	smps = []
	for j in range(N):
		db = Dots_Boxes(S)
		for i in np.random.permutation(S * (S - 1) * 2):
			db.lines[i] = 1
			if db.lines_to_score() >= 3:
				db.lines[i] = 0
		smps.append(db.lines.copy())
		action = np.random.choice(baseai(db))
		db.add_line(action)
		smps.append(db.lines.copy())
	return np.array(smps)

def sample_flip(sample, S):# Horizontal Flip
	fsmps = []
	for i in sample:
		fsmp = np.array([0] * S * (S - 1) * 2)
		for j, k in enumerate(i):
			if k == 1:
				if j < S * (S - 1):
					d = j % (S - 1)
					fsmp[j + S - 2 - 2 * d] = 1
				else:
					d = (j - S * (S - 1)) % S
					fsmp[j + S - 1 - 2 * d] = 1
		fsmps.append(fsmp)
	return np.array(fsmps)

def sample_angle90(sample, N, S):# Clockwise
	sp = sample.copy()
	for n in range(N):
		asmps = []
		for i in sp:
			asmp = np.array([0] * S * (S - 1) * 2)
			for j, k in enumerate(i):
				if k == 1:
					if j < S * (S - 1):
						d = j % (S - 1)
						n = j // (S - 1)
						asmp[S*(S-1+d) + (S-1) - n] = 1
					else:
						d = (j - S * (S - 1)) % S
						n = (j - S * (S - 1)) // S
						asmp[(S-1)*d + (S-2) - n] = 1
			asmps.append(asmp)
		sp = asmps.copy()
	return asmps

if __name__ == "__main__":
	import pandas as pd

	S = 5 # Game Size = 5
	Sps_o = samples(S, 70, 2) # 70 * 2 * 2(flip) * 4(rotate) = 1120 samples
	Sps_f = sample_flip(Sps_o, S)
	Sps = np.append(Sps_o, Sps_f, axis=0)

	Sps_1 = sample_angle90(Sps, 1, S)
	Sps_2 = sample_angle90(Sps, 2, S)
	Sps_3 = sample_angle90(Sps, 3, S)

	Samps = np.append(Sps, Sps_1, axis=0)
	Samps = np.append(Samps, Sps_2, axis=0)
	Samps = np.append(Samps, Sps_3, axis=0)
	print(len(Samps))
	print(len(np.unique(Samps, axis=0))) # Repeat detection.

	s = np.array([[0] * 100] * 140)
	for i, line in enumerate(Sps_o):
		for j in range(100):
			a = Dots_Boxes(5)
			a.lines = line
			while not a.end_game():
				if a.player == 1:
					action = np.random.choice(baseai(a))
					a = perform_action(a, action)
				else:
					a, _ = minimaxAB(a, 3)
			s[i, j] = a.score0

	sheu = pd.DataFrame(s)
	writer = pd.ExcelWriter('evaluate.xlsx')
	sheu.to_excel(writer, '1')
	writer.save()
	writer.close()

	samples = pd.DataFrame(Samps)
	writer = pd.ExcelWriter('samples.xlsx')
	samples.to_excel(writer, '1')
	writer.save()
	writer.close()

