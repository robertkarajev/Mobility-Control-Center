import pygame
import time as tm

class Window:
    def __init__(self, heigth, width):
        self.yDimension = 6
        self.xDimension = 6
        self.margin = 2
        self.heigth = (heigth + self.margin) * self.yDimension + self.margin
        self.width = (width + self.margin) * self.xDimension + self.margin
        self.windowSize = [self.heigth, self.width]
        self.window = pygame.display.set_mode(self.windowSize)

class Square:
    def __init__(self, state, color, coordY, coordX, width, height, margin, yPos, xPos):
        self.state = state
        self.color = color
        self.coordinateY = coordY
        self.coordinateX = coordX
        
        self.width = width
        self.height = height
        self.margin = margin
        self.yPosition = yPos + self.margin
        self.xPosition = xPos + self.margin

class Simulator:
    def __init__(self, grid, squareHeight, squareWidth):
        pygame.init()
        pygame.display.set_caption("Pathfinding Simulation") 
        
        self.window = Window(squareHeight, squareWidth)
        self.squares = []
        self.path = []

        self.prevPosition = None

        for row in range(self.window.yDimension):
            for column in range(self.window.xDimension):
                yPosition = (squareHeight + self.window.margin) * row
                xPosition = (squareWidth + self.window.margin) * column
                if grid[row][column] == 0:
                    self.squares.append(Square(0, roadColor, row, column, squareWidth, squareHeight, self.window.margin, yPosition, xPosition))
                if grid[row][column] == 1:
                    self.squares.append(Square(1, parkingSpaceColor, row, column, squareWidth, squareHeight, self.window.margin, yPosition, xPosition))
                if grid[row][column] == 2:
                    self.squares.append(Square(2, unusedSpaceColor, row, column, squareWidth, squareHeight, self.window.margin, yPosition, xPosition))

    #draws all the squares everytime this method is called
    def drawSquares(self):
        self.window.window.fill(backgroundColor)
        for square in self.squares:
            pygame.draw.rect(self.window.window, square.color, (square.xPosition, square.yPosition, square.width, square.height))
        pygame.display.flip()

    def simulateCarMovement(self, position, squares):
        coordY, coordX = position
        for square in squares:
            if self.prevPosition:
                prevCoordY, prevCoordX = self.prevPosition
                if square.coordinateY == prevCoordY and square.coordinateX == prevCoordX:
                    if square.state == 0:
                        square.color = roadColor
                    if square.state == 1:
                        square.color = parkingSpaceColor
            if square.coordinateY == coordY and square.coordinateX == coordX:
                square.color = carColor
                if square.state == 1 and len(self.path) == 1:
                    square.color = parkedSpaceColor
        self.drawSquares()

    def startSimulation(self):
        self.drawSquares()
        isRunning = True
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.path = self.getCoordsFromPath(path)
                        self.setPathColor(path, pathColor)
                        self.drawSquares()
                    if event.key == pygame.K_RIGHT:
                        self.simulateCarMovement(self.path[0], self.squares)
                        self.prevPosition = self.path[0]
                        self.path.pop(0)
                if event.type == pygame.QUIT:
                    isRunning = False
        pygame.quit()

    def getCoordsFromPath(self, path):
        filteredPath = []
        for coordinates in path:
            coordY, coordX, _ = coordinates
            filteredPath.append((coordY, coordX))
        return filteredPath

    def setPathColor(self, path, pathColor):
        for coordinates in path:
            coordY, coordX, _ = coordinates
            for square in self.squares:
                if square.coordinateY == coordY and square.coordinateX == coordX:
                    square.color = pathColor
                    break


unusedSpaceColor = (255, 0, 0)
backgroundColor = (0, 0, 0)

roadColor = (255, 255, 255)
pathColor = (120,30,50)
carColor = (255, 0, 212)

parkingSpaceColor = (0, 255, 0)
parkedSpaceColor = (255,140,0)

squareHeight = 45
squareWidth = 45

grid = [[2, 1, 1, 1, 0, 2, ],
        [1, 0, 0, 0, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 0, 0, 0, 1, ],
        [2, 0, 1, 1, 1, 2, ]]

path = [(5, 1, 'D'), (4, 1, 'D'), (3, 1, 'D'), (2, 1, 'D'), (1, 1, 'D'), (0, 1, 'D')]

simulator = Simulator(grid, squareHeight, squareWidth)
simulator.startSimulation()
simulator.setPathColor(path, pathColor)



#     def setPath(self, path):
#         self.path = path

#     def startGame(self):
#         path = self.path.copy()
#         isRunning = True
#         while isRunning:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     isRunning = False
#                 if event.type == pygame.KEYUP:
#                     self.grid = self.getRoute(path)
#                     self.simRoute(path)
#                     self.draw()
#                     if len(path) == 0:
#                         path = self.path.copy()
#         pygame.quit()

#     def getRoute(self, path):
#         counter=4
#         for cor in path:
#             coordY, coordX, direction = cor
#             self.grid[coordY][coordX]=counter
#             counter+=1
#         return self.grid

#     def simRoute(self,path):
#             coordY, coordX, direction = path[0]
#             self.grid[coordY][coordX] = 4
#             if self.prevCory:
#                 self.grid[self.prevCory][self.prevCorx] = 0
#             self.prevCory, self.prevCorx = coordY, coordX

#     def draw(self):
#         self.window.fill(self.BLACK)
#         for row in range(self.yDimension):
#             for column in range(self.xDimension):
#                 color = self.WHITE
#                 if self.grid[row][column] == 2:
#                     color = self.RED
#                 if self.grid[row][column] == 1:
#                     color = self.GREEN
#                 if self.grid[row][column] >= 5:
#                     color = self.PATHCOLOR
#                 if self.grid[row][column] == 0:
#                     color = self.WHITE
#                 if self.grid[row][column] == 4:
#                     color = self.PINK
#                 pygame.draw.rect(self.window, color, 
#                                  [(self.MARGIN + self.WIDTH) * column + self.MARGIN, 
#                                   (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
#                                   self.WIDTH, 
#                                   self.HEIGHT])
#         pygame.display.flip()

# # class Timer:
# #     def __init__(self):
# #         self.time = tm.time()

# #     def tick(self):
# #         self._oldtime = self.time
# #         self.time = tm.time()
# #         self.deltaTime = self.time - self._oldtime
# #         return self.deltaTime

# #time = Timer()
# # x=Visualize()
# # x.setPath([(5, 1, 'D'), (4, 1, 'D'), (3, 1, 'D'), (2, 1, 'D'), (1, 1, 'D'), (1, 1, 'D'), (1, 2, 'R'), (1, 3, 'R'), (1, 4, 'R'), (0, 4, 'D')])
# # x.startGame()