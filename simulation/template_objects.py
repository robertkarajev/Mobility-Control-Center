import pygame as pg
from ColorPalette import ColorPalette as cp

class TemplateObjects:
	def __init__(self, display, name, colour , position, size):
		self.display = display
		self.name = name
		self.colour = colour
		self.position = position[0],position[1],size[0],size[1]
		self.size = size

		self.select_colour(colour)
		self.object_interaction()
		self.insert_name_on_object()

	def create_object(self):
		pg.draw.rect(self.display, self.colour, self.position)

	def object_interaction(self):
		mouse_coords_x, mouse_coords_y = pg.mouse.get_pos()
		left_click, right_click, middle_click = pg.mouse.get_pressed()
		left, top, width, height = self.position

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

	def select_colour(self, RGB):
		if cp[str(RGB.upper())]:
			self.colour = cp[str(RGB.upper())].value

	def color_change_on_interaction(self):
		multiplier = 0.8
		r, g, b = self.colour
		if r >= 10:
			r = r * multiplier
		if g >= 10:
			g = g * multiplier
		if b >= 10:
			b = b * multiplier
		pg.draw.rect(self.display, (r,g,b), self.position)

	def attach_event_listener(self, execute_function = ""):
		try: 
			execute_function
		except:
			print("Warning -- no function attached")

	def insert_name_on_object(self):
		font_style = pg.font.Font("freesansbold.ttf", 12)
		text_line, text_position = self.attach_text_on_objects(self.name, font_style)
		text_position.center = ((self.position[0]+self.position[2]/2), (self.position[1]+self.position[3]/2))
		self.display.blit(text_line, text_position)

	def attach_text_on_objects(self, text, font):
		textSurface = font.render(text, True, cp["BLACK"].value)
		return textSurface, textSurface.get_rect()