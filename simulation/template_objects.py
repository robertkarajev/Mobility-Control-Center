import pygame as pg
from ColorPalette import ColorPalette as cp

class TemplateObjects:
	def __init__(self, display, name, colour , coordinates, size):
		self.display = display
		self.name = name
		self.colour = colour
		self.coordinates = coordinates
		self.size = size

		self.select_colour(colour)
		self.object_interaction()
		self.insert_name_on_object()

	def create_object(self):
		pg.draw.rect(self.display, self.colour, (self.coordinates, self.size))

	def select_colour(self, RGB):
		if cp[str(RGB.upper())]:
			self.colour = cp[str(RGB.upper())].value

	def object_interaction(self):
		mouse_coords_x, mouse_coords_y = pg.mouse.get_pos()
		left_click, right_click, middle_click = pg.mouse.get_pressed()
		left, top = self.coordinates
		width, height = self.size
		if (left+width) > mouse_coords_x > left and (top + height) > mouse_coords_y > top:
			self.color_change_on_interaction()
			if left_click:
				try:
					self.attach_event_listener()
					print("hello")
				except:
					SystemError
		else:
			self.create_object()            #reset to default

	def color_change_on_interaction(self):

		r, g, b = self.colour
		pg.draw.rect(self.display, (self.change_hsl(r),self.change_hsl(g),self.change_hsl(b)), self.coordinates)

	def change_hsl(self, given_colour):
		multiplier = 0.8
		if given_colour >= 10:
			given_colour = given_colour * multiplier
			return given_colour

	def attach_event_listener(self, execute_function = ""):
		try: 
			execute_function
		except:
			print("Warning -- no function attached")

	def insert_name_on_object(self):
		font_style = pg.font.Font("freesansbold.ttf", 12)
		text_line, text_position = self.attach_text_on_objects(self.name, font_style)
		text_position.center = ((self.coordinates[0]+self.size[0]/2), (self.coordinates[1]+self.size[1]/2))
		self.display.blit(text_line, text_position)

	def attach_text_on_objects(self, text, font):
		textSurface = font.render(text, True, cp["BLACK"].value)
		return textSurface, textSurface.get_rect()