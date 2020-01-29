import pygame as pg
from template_objects import TemplateObjects as tp
import math
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)
class Grid(tp):
    
    def __init__(self, display, name, colour, coordinates):
        super().__init__(display, name, colour, coordinates)
        self.grid_content = []
        self.coordinates = coordinates

    def draw_grid(self):
        for i in range( 41, 100 , 40):
            for j in range( 41, 400 , 40):   
                self.grid_content.append((i,j))
                pg.draw.rect(self.display, white, [i, j, 38, 38], 0)
    
                #pg.draw.rect(self.display, red, [81, 81, 38, 38], 0)

    def grid_interaction(self):
        mouse_coords_x, mouse_coords_y = pg.mouse.get_pos()
        left_click, right_click, middle_click = pg.mouse.get_pressed()
        left, top, width, height = self.coordinates
        #print(mouse_coords_x,mouse_coords_y)

        if left_click:              # Will be replaced with another function
            x = ((math.floor(mouse_coords_x/40))*40)+1
            
            y = ((math.floor(mouse_coords_y/40))*40)+1
            print(x)
            pg.draw.rect(self.display, red, [x, y, 38, 38], 0)

        # if (left+width) > mouse_coords_x > left and (top + height) > mouse_coords_y > top:
        #     if left_click:
        #         try:
        #             print("hello")
        #         except:
        #             SystemError
    
    def assign_grid(self):
        pass

    def validate_path(self):
        pass

    def resize_grid(self):
        width, height= self.display
        return ((width/2), (height/2))
