import pygame


testeheuristic = [
					["c","c","c","c","c","c","c","c","c","c"],
					["c","c","c","o","o","o","o","o","o","o"],
					["c","c","c","c","o","c","c","c","c","c"],
					["c","c","c","c","o","c","c","f","c","c"],
					["c","s","c","c","o","c","c","c","c","c"],
					["c","c","c","c","o","c","c","c","c","c"],
					["c","c","c","c","o","c","c","c","c","c"],
					["c","c","c","o","o","o","o","o","o","o"],
					["c","c","c","c","c","c","c","c","c","c"],
					["c","c","c","c","c","c","c","c","c","c"]
					]


def convert(gride):
	print(aaa)
	for x in range(len(grade)):
		for y in range(len(grade[1])):
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
				start = (x,y)
			if gride[x][y]=="f":
				gride[x][y] = block("end")
				end = (x,y)

	return gride,start,end


