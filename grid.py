
import pygame
import time

class Visualize(): 

    def __init__(self):
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.THEWAY = (120,30,50)
        self.RED = (255, 0, 0)
        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = 45
        self.HEIGHT = 45
        # This sets the margin between each cell
        self.MARGIN = 1
        self.grid = [
                        [2, 1, 1, 1, 0, 2, ],
                        [1, 0, 0, 0, 0, 1, ],
                        [1, 0, 1, 1, 0, 1, ],
                        [1, 0, 1, 1, 0, 1, ],
                        [1, 0, 0, 0, 0, 1, ],
                        [2, 0, 1, 1, 1, 2, ]
                        ]
        pygame.init()
        self.WINDOW_SIZE = [270, 270]
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
    

    def startPygame(self,routeCor):
        # Initialize pygame
            # Set title of screen
        pygame.display.set_caption("Array Backed Grid")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
                # -------- Main Program Loop -----------
        while not done:
            self.grid=self.route(routeCor)
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            # Set the screen background
            self.screen.fill(self.BLACK)
            self.draw()
            self.simRoute(routeCor)

            done=True
        self.stopPygame()



    def route(self,path):
        counter=3
        for cor in path:
            cory, corx, direction = cor
            self.grid[cory][corx]=counter
            counter+=1
        return self.grid


    # hier moet nog een waiter komen voor rfid tag: als gescaned is dan loop je door
    def simRoute(self,path):
        for index,cor in enumerate(path):
            cory, corx, direction = cor
            self.grid[cory][corx]=0
            self.draw()
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            time.sleep(1)
            


    def draw(self):
        for row in range(6):
            for column in range(6):
                color = self.WHITE
                if self.grid[row][column] == 2:
                    color = self.RED
                if self.grid[row][column] == 1:
                    color = self.GREEN
                if self.grid[row][column] >= 3:
                    color = self.THEWAY
                if self.grid[row][column] == 0:
                    color = self.WHITE
                pygame.draw.rect(self.screen,
                                    color,
                                    [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                    (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                    self.WIDTH,
                                    self.HEIGHT])

    def stopPygame(self):
        pygame.quit()


x=Visualize()
x.startPygame([(5, 1, 'D'), (4, 1, 'D'), (3, 1, 'D'), (2, 1, 'D'), (1, 1, 'D'), (1, 2, 'R'), (1, 3, 'R'), (1, 4, 'R'), (0, 4, 'D')])