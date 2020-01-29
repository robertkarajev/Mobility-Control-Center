import pygame as pg
import sys
from FunctionalButton import FunctionalButton as fb

pg.init()

size = (1280, 720)
display = pg.display.set_mode(size)
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)

display.fill(black)
pg.display.flip()

def create_buttons():
	redButton = fb(display, "redname", "red", 100, 300)				# Display, Name, colour, x-coords , y-coords, width , height
	blueButton = fb(display, "bluename" ,"blue", 200, 400)

def create_grid():
	for i in range( 41, size[0] - 200 , 40):
		for j in range( 41, size[1] -200 , 40):
			pg.draw.rect(display, white, [i, j, 38, 38], 0)
			pg.draw.rect(display, red, [81, 81, 38, 38], 0)
while True:
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()

	# pg.draw.rect(display, green,(150,450,100,50)) #Left, Top, width, Height
	# pg.draw.rect(display, red,(550,450,100,50))

	#mouse_coords_x, mouse_coords_y = pg.mouse.get_pos()
	#print(type(mouse_coords_x))
	#print(mouse_coords_x,"===", mouse_coords_y)
	create_grid()
	create_buttons()
	pg.display.update()
