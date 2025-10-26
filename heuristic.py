import snake
from snake import game
# import snakeTrain
# from snakeTrain import game

g = game()
while True:
	state = g.getState()
	if state[3] > 1e-9 and state[0] == 0:
		g.next([1,0,0])
	elif state[3] < -1e-9 and state[2] == 0:
		g.next([0,0,1])
	elif state[1] == 0:
		g.next([0,1,0])
	elif state[0] == 0:
		g.next([1,0,0])
	else:
		g.next([0,0,1])