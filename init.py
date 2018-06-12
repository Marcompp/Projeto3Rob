
import pygame
import random
from queue import Queue
from funcoes import priorityq



testemaze = [
					["c","g","g","c","c","c","c","o","c","o","o","c","c","c","o"],
					["o","c","c","o","c","c","c","c","c","o","c","c","o","o","o"],
					["c","c","c","c","c","s","c","o","c","o","c","c","c","o","o"],
					["c","o","c","c","c","o","c","c","c","o","c","c","c","c","o"],
					["c","s","c","c","c","c","c","c","c","o","c","c","f","c","o"],
					["c","c","c","c","c","c","c","c","c","o","c","c","c","c","o"],
					["c","c","c","c","c","c","c","c","c","o","c","c","c","c","o"],
					["c","c","c","o","o","o","o","o","o","o","c","c","c","c","o"],
					["c","c","c","c","c","c","c","c","c","c","c","c","c","c","o"],
					["c","c","c","c","c","c","c","c","c","c","c","c","c","c","o"]
					]

testeheuristic = [
					["c","g","g","g","c","c","c","c","c","c","c","c","c","c","o"],
					["c","c","c","o","o","o","o","o","o","o","c","w","w","w","o"],
					["c","c","c","c","c","c","c","c","c","o","c","w","w","w","o"],
					["c","c","c","c","c","c","c","o","c","o","c","c","c","c","o"],
					["c","s","c","c","c","c","c","c","c","o","c","c","f","c","o"],
					["c","c","c","c","c","c","c","c","c","o","c","c","c","c","o"],
					["c","c","c","c","c","c","c","c","c","o","c","c","c","c","o"],
					["c","c","c","o","o","o","o","o","o","o","c","c","g","g","o"],
					["c","c","c","c","w","w","w","w","w","c","c","c","g","g","o"],
					["c","c","c","c","c","c","c","c","c","c","c","c","c","c","o"]
					]

testedij = [
					["c","g","g","g","c","c","c","c","c","c","c","c","c","c","o"],
					["c","c","c","c","c","c","c","c","c","c","g","g","g","g","o"],
					["c","c","c","c","c","w","w","w","w","g","g","g","g","g","o"],
					["c","c","c","c","c","w","w","w","w","g","c","c","c","c","o"],
					["c","c","c","c","c","w","w","w","w","w","c","c","c","c","o"],
					["c","c","c","c","c","w","w","w","w","w","c","c","c","c","o"],
					["c","c","c","c","o","w","w","w","w","w","c","c","c","c","o"],
					["c","c","c","o","o","o","o","o","o","o","c","c","g","g","o"],
					["c","c","s","c","o","f","w","w","w","c","c","c","g","g","o"],
					["c","c","c","c","o","c","c","c","c","c","c","c","c","c","o"]
					]


class block:
	def __init__(self,ty):
		self.status = ty
		if ty == "obstacle":
			self.color = (50,50,50)
			self.cost = 100
		elif ty == "water":
			self.color = (155,155,165)
			self.cost = 3
		elif ty == "goal":
			self.color = (0,255,100)
			self.cost = 1
		elif ty == "grass":
			self.color = (185,185,185)
			self.cost = 2
		else:
			self.color = (215,215,215)
			self.cost = 1

	def refresh(self):
		if self.status == "obstacle":
			self.color = (50,50,50)
			self.cost = 100
		elif self.status == "water":
			self.color = (155,155,165)
			self.cost = 3
		elif self.status == "goal":
			self.color = (0,255,100)
			self.cost = 1
		elif self.status == "grass":
			self.color = (185,185,185)
			self.cost = 2
		else:
			self.color = (215,215,215)
			self.cost = 1

	def travel(self):
		self.color = (185,255,185)


	def become_frontier(self):
		self.color = (100,100,150)


width = 16
height = 10

def endar():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

def manhattan(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def generateterrain():
	grid = []
	for x in range(width-1):
		grid.append( [] )
		for y in range(height):
			i = random.randint(0,10)
			if i > 7:
				grid[x].append( block("obstacle") )
			elif i >5:
				grid[x].append( block("water") )
			elif i >3:
				grid[x].append( block("grass") )
			else:
				grid[x].append( block("clear") )
	for a in range(len(grid[1])):
		grid[-1][a] = block("obstacle")
	return grid


def convert(gride):
	for x in range(height):
		for y in range(width-1):
			if gride[x][y]=="c":
				gride[x][y] = block("clear")
			if gride[x][y]=="o":
				gride[x][y] = block("obstacle")
			if gride[x][y]=="w":
				gride[x][y] = block("water")
			if gride[x][y]=="g":
				gride[x][y] = block("grass")
			if gride[x][y]=="s":
				gride[x][y] = block("start")
				start = [y,x]
			if gride[x][y]=="f":
				gride[x][y] = block("end")
				end = [y,x]

	grid = []
	for x in range(width-1):
		grid.append( [] )
		for y in range(height):
			i = random.randint(0,10)
			if i > 8:
				grid[x].append( gride[y][x] )
			elif i >6:
				grid[x].append( gride[y][x] )
			elif i >4:
				grid[x].append( gride[y][x] )
			else:
				grid[x].append( gride[y][x] )
	return grid,start,end

def startpoint(grid):
	while True:
		x = random.randint(0,13)
		y = random.randint(0,height-2)
		if grid[x][y].status == "clear":
			return [x,y]

def displaycost(cost):
	letter = 30

	pygame.font.init()
	font_name = pygame.font.get_default_font()
	game_font = pygame.font.SysFont("Arial", letter)

	posx = 700
	posy = 30
	rect = pygame.Rect(posx,posy,40,45)
	pygame.draw.rect(gameDisplay, (205,205,205), rect)
	pygame.draw.rect(gameDisplay, (0,0,0), rect, 1)
	tex1 = game_font.render("{}".format(cost), 1, (0, 0, 0))
	gameDisplay.blit(tex1, (posx+5,posy+5))


def drawgrid(grid):
	block_size = wheight/height
	for x in range(width-1):
		for y in range(height):
			rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
			pygame.draw.rect(gameDisplay, grid[x][y].color, rect)
			pygame.draw.rect(gameDisplay, (0,0,0), rect, 1)

def drawstart(grid,start):
	x = start[0]
	y = start[1]
	block_size = wheight/height
	pygame.draw.circle(gameDisplay, (0,0,255), [int(x*block_size+block_size/2), int(y*block_size+block_size/2)], int(block_size/2))
	pygame.draw.circle(gameDisplay, (0,0,0), [int(x*block_size+block_size/2), int(y*block_size+block_size/2)], int(block_size/2),1)



def searchbfs(grid,start,end):
	frontier = Queue()
	frontier.put(start)
	came_from = {}
	came_from[start[0],start[1]] = None

	while not frontier.empty():
		current = frontier.get()
		if current[0] in range(len(grid)) and current[1] in range(len(grid[0])):
			grid[current[0]][current[1]].travel()
		#if current[0] in range(len(grid)) and current[1] in range(len(grid[0])):
			#grid[current[0]][current[1]].color = (185,255,185)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		if current == end: 
			break       
		neighbors = [[current[0]-1,current[1]],[current[0]+1,current[1]],[current[0],current[1]-1],[current[0],current[1]+1]]
		for next in neighbors:
			if (next[0],next[1]) not in came_from:
				if next[0] in range(len(grid)) and next[1] in range(len(grid[0])):
					if grid[next[0]][next[1]].status != "obstacle":
						frontier.put(next)

						grid[next[0]][next[1]].become_frontier()

						came_from[next[0],next[1]] = current

						if next == end:
							return came_from
			drawgrid(grid)
			drawstart(grid,start)
			pygame.display.update()
			clock.tick(60)
	return came_from


def searchdkt(grid,start,end):
	frontier = priorityq()
	frontier.put(start,0)
	came_from = {}
	came_from[start[0],start[1]] = None
	totcost = {}
	totcost[start[0],start[1]] = 0

	while not frontier.empty():
		current = frontier.get()
		grid[current[0]][current[1]].travel()


		if current == end: 
			break       
		neighbors = [[current[0]-1,current[1]],[current[0]+1,current[1]],[current[0],current[1]-1],[current[0],current[1]+1]]
		for next in neighbors:
			if next[0] in range(len(grid)) and next[1] in range(len(grid[0])):
				new_cost = totcost[current[0],current[1]] + grid[next[0]][next[1]].cost
				if (next[0],next[1]) not in totcost or new_cost < totcost[next[0],next[1]]:
					if grid[next[0]][next[1]].status != "obstacle":
						totcost[(next[0],next[1])] = new_cost
						priority = new_cost
						frontier.put(next, priority)

						grid[next[0]][next[1]].become_frontier()

						came_from[(next[0],next[1])] = current

						if next == end:
							return came_from
			drawgrid(grid)
			drawstart(grid,start)
			pygame.display.update()
			clock.tick(30)
	return came_from

def searchgbf(grid,start,end):
	frontier = priorityq()
	frontier.put(start,0)
	came_from = {}
	came_from[start[0],start[1]] = None

	while not frontier.empty():
		current = frontier.get()
		grid[current[0]][current[1]].travel()

		if current == end: 
			break       

		neighbors = [[current[0]-1,current[1]],[current[0]+1,current[1]],[current[0],current[1]-1],[current[0],current[1]+1]]
		for next in neighbors:
			if next[0] in range(len(grid)) and next[1] in range(len(grid[0])):
				if grid[next[0]][next[1]].status != "obstacle":
					if (next[0],next[1]) not in came_from:
						priority = manhattan(end,next)
						frontier.put(next, priority)

						grid[next[0]][next[1]].become_frontier()

						came_from[(next[0],next[1])] = current

						if next == end:
							return came_from
			drawgrid(grid)
			drawstart(grid,start)
			pygame.display.update()
			clock.tick(30)
	return came_from

def searchaaa(grid,start,end):
	frontier = priorityq()
	frontier.put(start,0)
	came_from = {}
	came_from[start[0],start[1]] = None
	totcost = {}
	totcost[start[0],start[1]] = 0

	while not frontier.empty():
		current = frontier.get()
		grid[current[0]][current[1]].travel()

		if current == end: 
			break       

		neighbors = [[current[0]-1,current[1]],[current[0]+1,current[1]],[current[0],current[1]-1],[current[0],current[1]+1]]
		for next in neighbors:
			if next[0] in range(len(grid)) and next[1] in range(len(grid[0])):
				new_cost = totcost[current[0],current[1]] + grid[next[0]][next[1]].cost
				if (next[0],next[1]) not in came_from:
					if grid[next[0]][next[1]].status != "obstacle":
						totcost[(next[0],next[1])] = new_cost
						priority = new_cost + manhattan(end,next)
						frontier.put(next, priority)

						grid[next[0]][next[1]].become_frontier()

						came_from[(next[0],next[1])] = current

						if next == end:
							return came_from
			drawgrid(grid)
			drawstart(grid,start)
			pygame.display.update()
			clock.tick(30)
	return came_from

def drawpath(came_from,start,end):
	if (end[0],end[1]) in came_from:
		blocksize = wheight/height
		current = end
		cost = 0
		while current != start:
			cost+= grid[current[0]][current[1]].cost
			#print(current)
			next = came_from[current[0],current[1]]
			#print(next)
			xstart = current[0] * blocksize + blocksize/2
			ystart = current[1] * blocksize + blocksize/2
			xend = next[0] * blocksize + blocksize/2
			yend = next[1] * blocksize + blocksize/2
			pygame.draw.line(gameDisplay, (255,0,0), (xstart,ystart), (xend,yend), 3)
			current = next
		displaycost(cost)




def menuinit():
	letter = 80

	pygame.font.init()
	font_name = pygame.font.get_default_font()
	game_font = pygame.font.SysFont("Arial", letter)


	lag =0
	cursor = 1
	clock = pygame.time.Clock()
	while True:
		endar()
		posx = 180
		rect = pygame.Rect(100,100,600,400)
		pygame.draw.rect(gameDisplay, (205,205,205), rect)
		pygame.draw.rect(gameDisplay, (0,0,0), rect, 1)
		posy = 125
		options = ["Breadth First","Dijkstra","Heuristic","A*"]
		y =0
		for tex in options:
			tex1 = game_font.render(tex, 1, (0, 0, 0))
			gameDisplay.blit(tex1, (posx,posy+y))
			y += letter

		pressed_keys = pygame.key.get_pressed()
		if lag >=5:
			if pressed_keys[pygame.K_UP]:
				cursor -=1
				lag = 0
			elif pressed_keys[pygame.K_DOWN]:
				cursor +=1
				lag = 0
			elif pressed_keys[pygame.K_LEFT]:
				cursor -=1
				lag = 0
			elif pressed_keys[pygame.K_RIGHT]:
				cursor +=1
				lag = 0
			elif pressed_keys[pygame.K_SPACE]:
				return cursor
		if cursor > len(options):
			cursor = len(options)
		if cursor <=0:
			cursor = 1
		if cursor == 1:
			tex1 = game_font.render(">", 1, (0, 0, 0))
			gameDisplay.blit(tex1, (posx-40,posy-5))
			#gameDisplay.blit(arrow(), (posx-15,posy-5))
		elif cursor == 2:
			tex1 = game_font.render(">", 1, (0, 0, 0))
			gameDisplay.blit(tex1, (posx-40,posy-5+letter))
			#gameDisplay.blit(arrow(), (posx-15,posy-5+letter))
		elif cursor == 3:
			tex1 = game_font.render(">", 1, (0, 0, 0))
			gameDisplay.blit(tex1, (posx-40, posy-5+letter*2))
			#gameDisplay.blit(arrow(), (posx-15,posy-5 + letter*2))
		elif cursor == 4:
			tex1 = game_font.render(">", 1, (0, 0, 0))
			gameDisplay.blit(tex1, (posx-40, posy-5+letter*3))
		lag+=1
		pygame.display.update()
		time_passed = clock.tick(30)




wheight = 600
wwidth = 840


maze = input("Modo: ")

pygame.init()

gameDisplay = pygame.display.set_mode((wwidth,wheight))
pygame.display.set_caption('A*')
clock = pygame.time.Clock()

if maze =="1":
	grid,start,end = convert(testeheuristic)
elif maze =="2":
	grid,start,end = convert(testedij)
else:
	grid = generateterrain()
	start = [1,1]
	end = [12,8]
	#start = startpoint(grid)
	#end = startpoint(grid)

grid[end[0]][end[1]] = block("goal")
grid[start[0]][start[1]] = block("start")



drawgrid(grid)
drawstart(grid,start)


search = menuinit()
while True:

	if search == 1:
		came_from =  searchbfs(grid,start,end)
	elif search == 2:
		came_from =  searchdkt(grid,start,end)
	elif search == 3:
		came_from =  searchgbf(grid,start,end)
	elif search == 4:
		came_from =  searchaaa(grid,start,end)

	for row in range(len(grid)):
		for columm in range(len(grid[1])):
			grid[row][columm].refresh()
		
	complete = True
	while complete:
		endar()
		drawgrid(grid)
		drawstart(grid,start)
		drawpath(came_from,start,end)
		
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_SPACE]:
			complete = False


		pygame.display.update()
		clock.tick(60)


	search = menuinit()
	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()