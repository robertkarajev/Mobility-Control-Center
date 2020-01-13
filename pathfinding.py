
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Pathfinding():
    grid = [
        [1, 1, 1, 1, 0, 1, ],
        [1, 0, 0, 0, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 0, 0, 0, 1, ],
        [1, 0, 1, 1, 1, 1, ]
    ]

    
    def astar(self,maze, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            # Adjacent squares (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), ]:

                # Get node position
                node_position = (
                    current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] > 0:
                    continue
                

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) **
                        2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def getGrid(self):
        return self.grid

    def alterGridForParkPlace(self,coordinates,park):
        xcor=coordinates[0]
        ycor=coordinates[1]
        if park:
            self.grid[xcor][ycor]=0
            return self.grid
        else:
            self.grid[xcor][ycor]=1
            return self.grid

    def setGrid(self,grid):
        self.grid=grid
    def getDirections(self,path):
        coor=path[0]
        ycor=coor[0]
        xcor=coor[1]
        pa=[]
        for index,cor in enumerate(path):
            cory = cor[0]
            corx = cor[1]
            try:
                if corx > path[index+1][1] or corx < path[index+1][1] :
                    pa.append((cory,corx,'R'))
                    ycor = cor[0]
                    xcor = cor[1]
                elif cory <= path[index+1][0] :
                    pa.append((cory,corx,'D'))
                    ycor = cor[0]
                    xcor = cor[1]
            except IndexError:
                pass
        return pa



#[(5, 1, 'D'), (4, 1, 'D'), (3, 1, 'D'), (2, 1, 'D'), (1, 1, 'D'), (1, 2, 'R'), (1, 3, 'R'), (1, 4, 'R'), (0, 4, 'D')]


def main():

    grid = [
        [1, 1, 1, 1, 0, 1, ],
        [1, 0, 0, 0, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 1, 1, 0, 1, ],
        [1, 0, 0, 0, 0, 1, ],
        [1, 0, 1, 1, 1, 1, ]
    ]
    start = (5,1)
    end = (0,4)


    pathfinding=Pathfinding()
    path=pathfinding.astar(grid, start, end)
    print(pathfinding.getDirections(path))


if __name__ == '__main__':
    main()
