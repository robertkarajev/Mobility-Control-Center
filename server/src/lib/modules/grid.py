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
                    self.squares.append(
                        Square(0, roadColor, row, column, squareWidth, squareHeight, self.window.margin, yPosition,
                               xPosition))
                if grid[row][column] == 1:
                    self.squares.append(
                        Square(1, parkingSpaceColor, row, column, squareWidth, squareHeight, self.window.margin,
                               yPosition, xPosition))
                if grid[row][column] == 2:
                    self.squares.append(
                        Square(2, unusedSpaceColor, row, column, squareWidth, squareHeight, self.window.margin,
                               yPosition, xPosition))

    # draws all the squares everytime this method is called
    def drawSquares(self):
        self.window.window.fill(backgroundColor)
        for square in self.squares:
            pygame.draw.rect(self.window.window, square.color,
                             (square.xPosition, square.yPosition, square.width, square.height))
        pygame.display.flip()

    def simulateCarMovement(self):
        if len(self.path) == 0:
            pygame.quit()
        #print(self.path)
        coordY, coordX = self.path[0]
        for square in self.squares:
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
        self.prevPosition = self.path[0]
        self.path.pop(0)

    def startSimulation(self):
        self.setPathColor()
        self.drawSquares()
        isRunning = True
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        #self.path = self.getCoordsFromPath()
                        self.setPathColor()
                        self.drawSquares()
                    if event.key == pygame.K_RIGHT:
                        if len(self.path) == 0:
                            isRunning = False
                            continue
                        self.simulateCarMovement()
                        self.prevPosition = self.path[0]
                        self.path.pop(0)
                if event.type == pygame.QUIT:
                    isRunning = False
        pygame.quit()

    '''def getCoordsFromPath(self):
        filteredPath = []
        for coordinates in self.path:
            coordY, coordX = coordinates
            filteredPath.append((coordY, coordX))
        return filteredPath
    '''

    def setPathColor(self):
        print(self.path)
        for coordinates in self.path:
            coordY, coordX = coordinates
            for square in self.squares:
                if square.coordinateY == coordY and square.coordinateX == coordX:
                    square.color = pathColor
                    break

    def setPath(self, path):
        self.path = path

unusedSpaceColor = (255, 0, 0)
backgroundColor = (0, 0, 0)

roadColor = (255, 255, 255)
pathColor = (120, 30, 50)
carColor = (255, 0, 212)

parkingSpaceColor = (0, 255, 0)
parkedSpaceColor = (255, 140, 0)

squareHeight = 45
squareWidth = 45

grid = [[2, 1, 1, 1, 0, 2, ],
        [1, 0, 0, 0, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 0, 0, 0, 1, ],
        [2, 0, 1, 1, 1, 2, ]]


def main():
    path = [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)]

    simulator = Simulator(grid, squareHeight, squareWidth)
    simulator.setPath(path)
    simulator.startSimulation()
    #simulator.setPathColor(pathColor)


if __name__ == '__main__':
    main()
