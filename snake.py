import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
	def __init__(self, start, rows, width, dirnx = 1, dirny = 0, color = (255, 0, 0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color
		self.rows = rows
		self.width = width

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		a = ((self.pos[0] + self.dirnx) % self.rows + self.rows) % self.rows
		b = ((self.pos[1] + self.dirny) % self.rows + self.rows) % self.rows
		self.pos = (a, b)

	def draw(self, surface, eyes = False):
		dis = self.width // self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
		if eyes:
			centre = dis // 2
			radius = dis // 6
			circleMiddle = (i * dis + centre - radius, j * dis + dis // 3)
			circleMiddle2 = (i * dis + dis - radius * 2, j * dis + dis // 3)
			pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
			pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos, rows, width):
		self.color = color
		self.head = cube(pos, rows, width)
		self.body.append(self.head)
		self.dirnx = 1
		self.dirny = 0
		self.rows = rows
		self.width = width

	def move(self, dir):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		
		if dir[0] == 1:
			ax = self.dirnx
			self.dirnx = self.dirny
			self.dirny = -ax
			self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
			
		elif dir[2] == 1:
			ax = self.dirnx
			self.dirnx = -self.dirny
			self.dirny = ax
			self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.dirnx = turn[0]
				c.dirny = turn[1]
				if i == len(self.body) - 1:
					self.turns.pop(p)
			c.move(c.dirnx, c.dirny)



	def reset(self, pos, rows, width):
		self.head = cube(pos, rows, width)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 1
		self.dirny = 0
		self.rows = rows
		self.width = width

	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0] - 1, tail.pos[1]), self.rows, self.width))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0] + 1, tail.pos[1]), self.rows, self.width))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0], tail.pos[1] - 1), self.rows, self.width))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0], tail.pos[1] + 1), self.rows, self.width))

		a = (self.body[-1].pos[0] % self.rows + self.rows) % self.rows
		b = (self.body[-1].pos[1] % self.rows + self.rows) % self.rows
		self.body[-1].pos = (a, b)

		self.body[-1].dirnx = dx;
		self.body[-1].dirny = dy;

	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)

def drawGrid(width, rows, surface):
	sizeBetween = width // rows

	x = 0
	y = 0
	for l in range(rows):
		x = x + sizeBetween
		y = y + sizeBetween

		pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
		pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))

def drawScore(surface, rows, width, s, highest):
	font = pygame.font.Font('freesansbold.ttf', width // rows * 5 // 6) 
	text = font.render('SCORE: ' + str(len(s.body) - 1), True, (255, 255, 255), (0, 0, 0)) 
	textRect = text.get_rect()
	textRect.center = (width // 9, width + width // rows // 2)
	surface.blit(text, textRect)

	font = pygame.font.Font('freesansbold.ttf', width // rows * 5 // 6) 
	text = font.render('HIGHEST: ' + str(highest), True, (255, 255, 255), (0, 0, 0)) 
	textRect = text.get_rect()
	textRect.center = (6 * width // 7, width + width // rows // 2)
	surface.blit(text, textRect)

def redrawWindow(surface, rows, width, s, snack, highest):
	surface.fill((0,0,0))
	snack.draw(surface)
	s.draw(surface)
	drawGrid(width, rows, surface)
	drawScore(surface, rows, width, s, highest)
	
	pygame.display.update()

def randomCube(rows):
	x = random.randrange(rows)
	y = random.randrange(rows)
	return (x, y)

def randomSnack(rows, snake):
	positions = snake.body

	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: 
			continue
		else:
			break
	return (x, y)

def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass

		
# class game(object):
# 	def __init__(self)


class game(object):

	def __init__(self, rows = 20, width = 400):
		pygame.init()
		self.rows = rows
		self.width = width
		self.surface = pygame.display.set_mode((self.width, self.width + self.width // self.rows))
		pygame.display.set_caption('Snake :)')
		self.s = snake((255,0,0), randomCube(self.rows), self.rows, self.width)
		self.snack = cube(randomSnack(self.rows, self.s), self.rows, self.width, color = (0, 255, 0))
		self.highest = 0
		self.games = 0
		self.prom = 0
		self.clock = pygame.time.Clock()

		redrawWindow(self.surface, self.rows, self.width, self.s, self.snack, self.highest)

	def getRows(self):
		return self.rows

	def next(self, dir = [0,0,0]):
		pygame.time.delay(5)
		self.clock.tick(100)
		self.s.move(dir)
		if self.s.body[0].pos == self.snack.pos:
			self.s.addCube()
			self.snack = cube(randomSnack(self.rows, self.s), self.rows, self.width, color = (0, 255, 0))

		if(self.s.body[0].pos in list (map(lambda z:z.pos,self.s.body[1:]))):
			self.prom = self.prom * self.games;
			self.prom = self.prom + len(self.s.body) - 1
			self.games = self.games + 1
			self.prom = self.prom / self.games
			print(' Game #' + str(self.games), ' Score: ', len(self.s.body) - 1, ' Average: ', self.prom, ' Highest: ', self.highest)
			message_box('You Lost!', 'Play again...')
			self.s.reset(randomCube(self.rows), self.rows, self.width)

		self.highest = max(self.highest, len(self.s.body) - 1)
		redrawWindow(self.surface, self.rows, self.width, self.s, self.snack, self.highest)
		
	def getState(self):
		n = self.rows
		table = []
		for i in range(0,n):
			aux = []
			for j in range(0,n):
				x = 0
				aux.append(x)
			table.append(aux)

		for i in range(len(self.s.body)):
			if(i == 0):
				table[self.s.body[i].pos[0]][self.s.body[i].pos[1]] = 1
			else:	
				table[self.s.body[i].pos[0]][self.s.body[i].pos[1]] = 2

		table[self.snack.pos[0]][self.snack.pos[1]] = 3

		snack = self.snack.pos
		head = self.s.body[0]
		pos = head.pos
		state = [0,0,0,0]
		if head.dirnx == 1:
			if table[pos[0]][(pos[1] - 1 + self.rows) % self.rows] == 2:
				state[0] = 1
			if table[(pos[0] + 1) % self.rows][pos[1]] == 2:
				state[1] = 1
			if table[pos[0]][(pos[1] + 1) % self.rows] == 2:
				state[2] = 1
			state[3] = math.sin(math.atan2(pos[1] - snack[1], snack[0] - pos[0]))
		elif head.dirnx == -1:
			if table[pos[0]][(pos[1] + 1) % self.rows] == 2:
				state[0] = 1
			if table[(pos[0] - 1 + self.rows) % self.rows][pos[1]] == 2:
				state[1] = 1
			if table[pos[0]][(pos[1] - 1 + self.rows) % self.rows] == 2:
				state[2] = 1
			state[3] = math.sin(math.atan2(snack[1] - pos[1], pos[0] - snack[0]))
		elif head.dirny == 1:
			if table[(pos[0] + 1) % self.rows][pos[1]] == 2:
				state[0] = 1
			if table[pos[0]][(pos[1] + 1) % self.rows] == 2:
				state[1] = 1
			if table[(pos[0] - 1 + self.rows) % self.rows][pos[1]] == 2:
				state[2] = 1
			state[3] = math.sin(math.atan2(snack[0] - pos[0], snack[1] - pos[1]))
		else:
			if table[(pos[0] - 1 + self.rows) % self.rows][pos[1]] == 2:
				state[0] = 1
			if table[pos[0]][(pos[1] - 1 + self.rows) % self.rows] == 2:
				state[1] = 1
			if table[(pos[0] + 1) % self.rows][pos[1]] == 2:
				state[2] = 1
			state[3] = math.sin(math.atan2((pos[0] - snack[0]) , (pos[1] - snack[1])))

		return state
	def end(self):
		pygame.quit()


