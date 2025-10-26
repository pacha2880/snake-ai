class game(object):

	def __init__(self):
		pygame.init()
		self.rows = 10
		self.width = 400
		self.surface = pygame.display.set_mode((self.width, self.width + self.width // self.rows))
		pygame.display.set_caption('Snake :)')
		self.s = snake((255,0,0), randomCube(self.rows), self.rows, self.width)
		self.snack = cube(randomSnack(self.rows, self.s), self.rows, self.width, color = (0, 255, 0))
		self.highest = 0

		self.clock = pygame.time.Clock()

		redrawWindow(self.surface, self.rows, self.width, self.s, self.snack, self.highest)

	def next(self, dir = [0,1,0]):
		self.s.move(dir)
		if self.s.body[0].pos == self.snack.pos:
			self.s.addCube()
			self.snack = cube(randomSnack(self.rows, self.s), self.rows, self.width, color = (0, 255, 0))

		if(self.s.body[0].pos in list (map(lambda z:z.pos,self.s.body[1:]))):
			print('Score: ', len(self.s.body))
			message_box('You Lost!', 'Play again...')
			self.s.reset(randomCube(self.rows), self.rows, self.width)

		self.highest = max(self.highest, len(self.s.body) - 1)
		redrawWindow(self.surface, self.rows, self.width, self.s, self.snack, self.highest)
		
	def getState(self):
		n = self.rows
		state = [[0] * n] * n

		for i in range(len(state)):
			print(state[i])	

		for i in range(len(self.s.body)):
			if i == 0:
				state[self.s.body[i].pos[0]][self.s.body[i].pos[1]] = 1
			else:
				state[self.s.body[i].pos[0]][self.s.body[i].pos[1]] = 2

		state[self.snack.pos[0]][self.snack.pos[1]] = 1

		for i in range(len(state)):
			print(state[i])	