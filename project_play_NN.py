from project_state import *
from project_ai import *
from project_NN import *
from time import time
import torch as tr

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
	print('Please wait for NN training...')

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

	print('Training finished.')
	
	players = ['Human Player', 'Baseline AI', 'Tree-based AI', 'Tree+NN AI']

	print('This game is played at size of 5.\n Dots are numbered as following:\n  0    1    2    3    4\n  5    6    7    8    9\n 10   11   12   13   14\n 15   16   17   18   19\n 20   21   22   23   24')
	print('Lines of boxes are numbered as following:\n  o  0 o  1 o  2 o  3 o\n 20   21   22   23   24\n  o  4 o  5 o  6 o  7 o\n 25   26   27   28   29\n  o  8 o  9 o 10 o 11 o\n 30   31   32   33   34\n  o 12 o 13 o 14 o 15 o\n 35   36   37   38   39\n  o 16 o 17 o 18 o 19 o\n\n')

	rechoose = 1
	while(rechoose == 1):
		ipt1 = 'Input 0, 1, 2, 3 for Player A.\n 0 = Human Player\n 1 = Baseline AI\n 2 = Tree-based AI\n 3 = Tree+NN AI\n'
		player1 = -1
		while(player1 not in [0, 1, 2, 3]):
			player1 = int(input(ipt1))

		ipt2 = f'Input 0, 1, 2, 3 for Player A.\n 0 = Human Player\n 1 = Baseline AI\n 2 = Tree-based AI\n 3 = Tree+NN AI\n'
		player2 = -1
		while(player2 not in [0, 1, 2, 3]):
			player2 = int(input(ipt2))

		print(f'Player A:{players[player1]}\nPlayer B:{players[player2]}\n')

		ctn = 'Press Enter to continue.\n'
		input(ctn)

		a = Dots_Boxes(5)
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
				elif player1 == 2:
					input(ctn)
					start = time()
					a, _ = minimaxAB(a, 3, AI=a.player)
					stop = time()
					print(str(stop-start) + "s")
				else:
					input(ctn)
					start = time()
					a, _ = minimaxAB(a, 3, AI=a.player, evaluator=evaluator_nn)
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
				elif player2 == 2:
					input(ctn)
					start = time()
					a, _ = minimaxAB(a, 3, AI=a.player)
					stop = time()
					print(str(stop-start) + "s")
				else:
					input(ctn)
					start = time()
					a, _ = minimaxAB(a, 3, AI=a.player, evaluator=evaluator_nn)
					stop = time()
					print(str(stop-start) + "s")

		a.show()
		print('Score for Player A: ', a.score0)
		print('Score for Player B: ', a.score1)
		print(f'Player A: {players[player1]} wins!' if a.score > 0 else f'Player B: {players[player2]} wins!' if a.score < 0 else 'Tied!')

		iptrc = '\nEnter 1 for another game, or 0 for quitting.\n'
		rechoose = int(input(iptrc))
		while(rechoose not in [0, 1]):
			rechoose = int(input(iptrc))
