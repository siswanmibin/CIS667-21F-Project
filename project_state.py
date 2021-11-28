import numpy as np
import copy

# dots are numbered as following:
#  0    1    2    3
#  4    5    6    7
#  8    9   10   11
# 12   13   14   15

# lines of boxes are numbered as following:
#  o  0 o  1 o  2 o
# 12   13   14   15
#  o  3 o  4 o  5 o
# 16   17   18   19
#  o  6 o  7 o  8 o
# 20   21   22   23
#  o  9 o 10 o 11 o

class Dots_Boxes:
	def __init__(self, SIZE=3):
		self.SIZE = SIZE
		self.lines = np.array([0] * SIZE * (SIZE - 1) * 2)
		self.player = 0
		self.score = 0
		self.score0 = 0
		self.score1 = 0
		self.change = 0
		self.scores = ['  '] * ((SIZE - 1) ** 2)

	def valid_actions(self):
		return np.where((self.lines==0))[0]

	def lines_dots(self, n): # n between 0, 2*SIZE*(SIZE-1)-1
		S = self.SIZE
		if n < S*(S-1):
			i = n // (S-1)
			j = n % (S-1)
			return (i*S+j), (i*S+j+1)
		else:
			return (n-S*(S-1)), (n-S*(S-2))

	def dots_line(self, m, n): # n = m + 1 or n = m + SIZE
		S = self.SIZE
		i, j = min(m, n), max(m, n)
		if j == i + 1:
			return i % S + (i // S)*(S - 1)
		elif j == i + S:
			return i + S*(S-1)
		else:
			return False

	def score_aeras(self):
		S = self.SIZE - 1
		sa = []
		for i in range(S**2):
			j = i // S
			l1 = i
			l2 = i + S*(S+1)+j
			l3 = i + S
			l4 = l2 + 1
			sa.append(((l1, l2, l3, l4), (self.lines[l1], self.lines[l2], self.lines[l3], self.lines[l4])))
		return sa

	def new_scores(self, i, p):
		self.scores[i] = '-1' if p else '+1'

	def is_bonus_action_of(self, n): # if add line n can get score
		sa = self.score_aeras()
		aeras = []
		for i in range(len(sa)):
			if n in sa[i][0] and sum(sa[i][1]) == 3:
				aeras.append(i)
		if aeras:
			return aeras
		else:
			return []

	def lines_to_score(self): # if add any line can get score
		for n in self.valid_actions():
			if self.is_bonus_action_of(n):
				return 1
		return 0

	def add_line(self, n):
		if len(self.is_bonus_action_of(n)) > 0:
			for aera in self.is_bonus_action_of(n):
				self.new_scores(aera, self.player)
				s = -1 if self.player else 1
				self.score += s
				if self.player:
					self.score1 += 1
				else:
					self.score0 += 1
			self.lines[n] = 1
			self.change = 1
		else:
			self.player = 1 - self.player
			self.lines[n] = 1
		return 1

	def end_game(self):
		if self.lines.all():
			return True
		return False

	def get_symbol(self, n):
		S = self.SIZE
		L = S * 2 - 1
		i = n // L
		j = n % L
		A = '  '
		B = 'o'
		C = '=='
		D = '|'
		d = ' '
		if i % 2:
			if j % 2:
				return self.scores[int((S-1)*(i-1)/2 + (j-1)/2)]
			else:
				return D if self.lines[int(S*(S-1)+S*(i-1)/2+j/2)]==1 else d
		else:
			if j % 2:
				return C if self.lines[int((i/2)*(S-1)+(j-1)/2)]==1 else A
			else:
				return B

	def show(self):
		l = []
		S = self.SIZE
		print('---', ['A', 'B'][self.player], ' turn ---')
		for i in range((S * 2 - 1)**2):
			l.append(self.get_symbol(i))
			if i % (S*2-1) == S*2-2:
				l.append('\n')
		print(''.join(l))

def perform_action(DB, n):
	cp = copy.deepcopy(DB)
	cp.add_line(n)
	return cp

if __name__ == "__main__":
	a = Dots_Boxes(3)
	while(1):
		a.show()
		print(a.score_aeras())
		if len(a.valid_actions()) > 0:
			j = np.random.choice(a.valid_actions())
		else: break
		print(a.is_bonus_action_of(j))
		a = perform_action(a, j)
	print('Net Score: ', a.score)
	print('A win!' if a.score > 0 else 'B win!' if a.score < 0 else 'Tied!')
