
import pygame

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
    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    

    def startPygame(self,routeCor):
            # Initialize pygame
        pygame.init()
        WINDOW_SIZE = [270, 270]
        screen = pygame.display.set_mode(WINDOW_SIZE)
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    # Set that location to one
                    grid[row][column] = 0
                    print("Click ", pos, "Grid coordinates: ", row, column)

            # Set the screen background
            screen.fill(self.BLACK)

            # Draw the grid
            for row in range(6):
                for column in range(6):

                    color = self.WHITE
                    if self.grid[row][column] == 2:
                        color = self.RED
                    if self.grid[row][column] == 1:
                        color = self.GREEN
                    if self.grid[row][column] >= 3:
                        color = self.THEWAY
                    pygame.draw.rect(screen,
                                        color,
                                        [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                        (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                        self.WIDTH,
                                        self.HEIGHT])
            # Limit to 60 frames per second
            clock.tick(60)
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        self.stopPygame()



    def route(self,path):
        counter=3
        for cor in path:
            cory, corx, direction = cor
            self.grid[cory][corx]=counter
            counter+=1
        return self.grid



    def stopPygame(self):
        pygame.quit()


x=Visualize()
x.startPygame([(5, 1, 'D'), (4, 1, 'D'), (3, 1, 'D'), (2, 1, 'D'), (1, 1, 'D'), (1, 2, 'R'), (1, 3, 'R'), (1, 4, 'R'), (0, 4, 'D')])