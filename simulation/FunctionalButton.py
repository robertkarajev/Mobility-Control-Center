import pygame as pg
from template_objects import TemplateObjects as tp

class FunctionalButton(tp):
	def __init__(self, display, name, colour, coordinates):
		super().__init__(display, name, colour, coordinates)
			
	# def __init__(self, display, name = "default", colour = "gray", x_coords = 150, y_coords = 450, width = 100, height = 50):		
		
	# 	self.name = name
	# 	self.colour = (128,128,128)									# Red,Green,Blue // default parameters
	# 	self.position = (x_coords, y_coords, width, height)			#Left, Top, Width, Height
	# 	self.display = display
	# 	self.width = width
	# 	self.height = height

	# 	self.select_colour(colour)
	# 	self.button_interaction()
	# 	self.add_text_on_button()

	# def add_text_on_button(self):
	# 	font_style = pg.font.Font("freesansbold.ttf", 12)
	# 	text_line, text_position = self.text_objects(self.name, font_style)
	# 	text_position.center = ((self.position[0]+self.position[2]/2), (self.position[1]+self.position[3]/2))
	# 	self.display.blit(text_line, text_position)

	# def text_objects(self, text, font):
	# 	textSurface = font.render(text, True, cp["BLACK"].value)
	# 	return textSurface, textSurface.get_rect()

	# def color_change_on_selection(self):
	# 	multiplier = 0.8
	# 	r, g, b = self.colour
	# 	if r >= 10:
	# 		r = r * multiplier
	# 	if g >= 10:
	# 		g = g * multiplier
	# 	if b >= 10:
	# 		b = b * multiplier
	# 	pg.draw.rect(self.display, (r,g,b), self.position)

		
		
		
		