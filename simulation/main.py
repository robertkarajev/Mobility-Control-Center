import pygame as pg
import sys
from Grid import Grid as gd

pg.init()

size = (1280, 720)
display = pg.display.set_mode(size)
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)

display.fill(black)
pg.display.flip()

new_grid = gd(display,"grid1","gray", (100,100,100,100)) # display, name, colour , position (top, left , width , height)
new_grid.draw_grid()


while True:
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
	new_grid.grid_interaction()
	
	

	pg.display.update()
