#Snake tutorial Python

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
		self.dirnx = 0
		self.dirny = 1
		self.rows = rows
		self.width = width

	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[pygame.K_LEFT] and (self.dirnx != 1 or len(self.body) < 2):
					self.dirnx = -1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_RIGHT] and (self.dirnx != -1 or len(self.body) < 2):
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					
				elif keys[pygame.K_UP] and (self.dirny != 1 or len(self.body) < 2):
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					
				elif keys[pygame.K_DOWN] and (self.dirny != -1 or len(self.body) < 2):
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body) - 1:
					self.turns.pop(p)
			else:
				c.move(c.dirnx, c.dirny)



	def reset(self, pos, rows, width):
		self.head = cube(pos, rows, width)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1
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

		a = ((self.body[-1].pos[0]) % self.rows + self.rows) % self.rows
		b = ((self.body[-1].pos[1]) % self.rows + self.rows) % self.rows
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

def main():
	pygame.init()
	rows = 20
	width = 400
	surface = pygame.display.set_mode((width, width + width // rows))
	pygame.display.set_caption('Snake :)')
	s = snake((255,0,0), randomCube(rows), rows, width)
	snack = cube(randomSnack(rows, s), rows, width, color = (0, 255, 0))
	flag = True
	highest = 0
	games = 0
	prom = 0
	clock = pygame.time.Clock()

	while flag:
		pygame.time.delay(20)
		clock.tick(15)
		s.move()
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows, s), rows, width, color = (0, 255, 0))

		if(s.body[0].pos in list (map(lambda z:z.pos,s.body[1:]))):
			prom = prom * games
			prom = prom + len(s.body) - 1
			games = games + 1
			prom = prom / games
			print(' Game #' + str(games), ' Score: ', len(s.body) - 1, ' Average: ', prom, ' Highest: ', highest)
			games = games + 1
			message_box('You Lost!', 'Play again...')
			s.reset(randomCube(rows), rows, width)
			#break

		highest = max(highest, len(s.body) - 1)
		redrawWindow(surface, rows, width, s, snack, highest)

	pass

main()

		
# class game(object):
# 	def __init__(self)

class point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def printp(self):
		print(self.x, self.y)