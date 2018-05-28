import pygame
import random
from queue import Queue
from funcoes import priorityq



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
		else:
			self.color = (215,215,215)
			self.cost = 1

	def become_frontier(self):
			self.color = (100,100,150)		


width = 16
height = 10

def manhattan(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def generateterrain():
	grid = []
	for x in range(width):
		grid.append( [] )
		for y in range(height):
			i = random.randint(0,10)
			if i > 8:
				grid[x].append( block("obstacle") )
			elif i >6:
				grid[x].append( block("water") )
			else:
				grid[x].append( block("clear") )
	return grid

def startpoint(grid):
	while True:
		x = random.randint(0,width-2)
		y = random.randint(0,height-2)
		if grid[x][y].status == "clear":
			return [x,y]

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
				frontier.put(next)
				grid[next[0]][next[1]].become_frontier()
				came_from[next[0],next[1]] = current
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
		grid[current[0]][current[1]].color = (185,255,185)


		if current == end: 
			break       
		neighbors = [[current[0]-1,current[1]],[current[0]+1,current[1]],[current[0],current[1]-1],[current[0],current[1]+1]]
		for next in neighbors:
			if next[0] in range(len(grid)) and next[1] in range(len(grid[0])):
				new_cost = totcost[current[0],current[1]] + grid[next[0]][next[1]].cost
				if (next[0],next[1]) not in totcost or new_cost < totcost[next[0],next[1]]:
					totcost[(next[0],next[1])] = new_cost
					priority = new_cost
					frontier.put(next, priority)
					came_from[(next[0],next[1])] = current

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
	totcost = {}
	totcost[start[0],start[1]] = 0

	while not frontier.empty():
		current = frontier.get()
		grid[current[0]][current[1]].color = (185,255,185)

		if current == end: 
			break       

		neighbors = [[current[0]-1,current[1]],[current[0]+1,current[1]],[current[0],current[1]-1],[current[0],current[1]+1]]
		for next in neighbors:
			if next[0] in range(len(grid)) and next[1] in range(len(grid[0])):
				new_cost = totcost[current[0],current[1]] + grid[next[0]][next[1]].cost
				if (next[0],next[1]) not in came_from:
					totcost[(next[0],next[1])] = new_cost
					priority = new_cost + manhattan(end,next)
					frontier.put(next, priority)
					came_from[(next[0],next[1])] = current

			drawgrid(grid)
			drawstart(grid,start)
			pygame.display.update()
			clock.tick(30)
	return came_from

def drawpath(came_from,start,end):
	blocksize = wheight/height
	current = end
	while current != start:
		print(current)
		next = came_from[current[0],current[1]]
		print(next)
		xstart = current[0] * blocksize + blocksize/2
		ystart = current[1] * blocksize + blocksize/2
		xend = next[0] * blocksize + blocksize/2
		yend = next[1] * blocksize + blocksize/2
		pygame.draw.line(gameDisplay, (255,0,0), (xstart,ystart), (xend,yend), 3)
		current = next


wheight = 600
wwidth = 840




pygame.init()

gameDisplay = pygame.display.set_mode((wwidth,wheight))
pygame.display.set_caption('A*')
clock = pygame.time.Clock()

grid = generateterrain()

start = startpoint(grid)
grid[start[0]][start[1]] = block("start")
end = startpoint(grid)
grid[end[0]][end[1]] = block("goal")

crashed = False


came_from =  searchgbf(grid,start,end)


while not crashed:
    drawgrid(grid)
    drawstart(grid,start)
    drawpath(came_from,start,end)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        #print(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()