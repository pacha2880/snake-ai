import snake
from snake import game
# import snakeTrain
# from snakeTrain import game
left = True
cross = False
g = game()
con = g.getRows() - 2
while True:
	state = g.getState()
	if cross:
		if left:
			g.next([1,0,0])
			left = False
		else:
			g.next([0,0,1])
			left = True
		cross = False
		con = g.getRows() - 2
	elif con == 0:
		if left:
			g.next([1,0,0])
			cross = True
		else:
			g.next([0,0,1])
			cross = True
	else:
		con = con - 1
		g.next([0,1,0])