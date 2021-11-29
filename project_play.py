from project_state import *
from project_ai import *
from time import time

def get_user_action(dotsboxes):
	actions = dotsboxes.valid_actions()
	actiondots = [dotsboxes.lines_dots(n) for n in actions]
	p = 'B' if dotsboxes.player else 'A'
	prompt = f'Valid lines: {dotsboxes.valid_actions()}\nPlayer {p}, enter two numbers FOR dots separated by space, OR a single number FOR a line:\n'
	while 1:
		action = input(prompt).split()
		if len(action) == 2:
			try:
				d1, d2 = int(action[0]), int(action[1])
				if ((d1, d2) in actiondots) or ((d2, d1) in actiondots):
					return dotsboxes.dots_line(d1, d2)
			except:
				1
		elif len(action) == 1:
			try:
				d = int(action[0])
				if d in actions:
					return d
			except:
				1
		print("Invalid action, try again.")


if __name__ == "__main__":
	players = ['Human Player', 'Baseline AI', 'Tree-based AI']

	ipt = 'Enter a number from (2, 3, 4, 5, 6) for size: '
	print(' Dots are numbered as following:\n  0    1    2    3\n  4    5    6    7\n  8    9   10   11\n 12   13   14   15\n Lines of boxes are numbered as following:\n  o  0 o  1 o  2 o\n 12   13   14   15\n  o  3 o  4 o  5 o\n 16   17   18   19\n  o  6 o  7 o  8 o\n 20   21   22   23\n  o  9 o 10 o 11 o\n\n')
	size = 0
	while(size not in [2, 3, 4, 5, 6]):
		size = int(input(ipt))

	ipt1 = 'Input 0, 1, 2 for Player A.\n 0 = Human Player\n 1 = Baseline AI\n 2 = Tree-based AI\n'
	player1 = -1
	while(player1 not in [0, 1, 2]):
		player1 = int(input(ipt1))

	ipt2 = f'Input 0, 1, 2 for Player A.\n 0 = Human Player\n 1 = Baseline AI\n 2 = Tree-based AI\n'
	player2 = -1
	while(player2 not in [0, 1, 2]):
		player2 = int(input(ipt2))

	print(f'Player A:{players[player1]}\nPlayer B:{players[player2]}\n')

	ctn = 'Press Enter to continue.\n'
	input(ctn)

	a = Dots_Boxes(size)
	while not a.end_game():
		a.show()
		if a.player == 0:
			if player1 == 0:
				action = get_user_action(a)
				a = perform_action(a, action)
			elif player1 == 1:
				input(ctn)
				action = np.random.choice(baseai(a))
				a = perform_action(a, action)
			else:
				input(ctn)
				start = time()
				a, _ = minimaxAB(a, 3, AI=a.player)
				stop = time()
				print(str(stop-start) + "s")
		else:
			if player2 == 0:
				action = get_user_action(a)
				a = perform_action(a, action)
			elif player2 == 1:
				input(ctn)
				action = np.random.choice(baseai(a))
				a = perform_action(a, action)
			else:
				input(ctn)
				start = time()
				a, _ = minimaxAB(a, 3, AI=a.player)
				stop = time()
				print(str(stop-start) + "s")

	a.show()
	print('Score for Player A: ', a.score0)
	print('Score for Player B: ', a.score1)
	print(f'Player A: {players[player1]} wins!' if a.score > 0 else f'Player B: {players[player2]} wins!' if a.score < 0 else 'Tied!')
