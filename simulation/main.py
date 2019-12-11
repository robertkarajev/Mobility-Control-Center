import pygame as pg
import sys
from Grid import Grid as gd
from template_objects import TemplateObjects as tp


pg.init()

size = (1280, 720)
display = pg.display.set_mode(size)
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)

display.fill(white)
pg.display.flip()

new_tp = tp(display,"test","red",(500,500),(150,150))

while True:
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
	# new_grid.grid_interaction()
	
	

	pg.display.update()
