import random, pygame, sys, numpy as np    # import libraries

from Maze_Solving import ActiveNode    # a variation on the solving algorithm is used when checking which corridors are connected to maze entrance - needs ActiveNode class


pygame.init()


WHITE = [255, 255, 255]
BLACK = [  0,   0,   0]
GREEN = [  0, 255,   0]
RED   = [255,   0,   0]





##
##                 Maze structure:
##     Maze is stored as a 2d array of numbers (data type numpy.array)
##     1 is a maze wall, all other numbers are corridors
##     0 is an unmarked corridor
##     9 is the entrance to the maze, 8 is the exit
##     2s are connected to the entrance of the maze, 4s are not connected
##     3s are currently being processed
##     7s mark the shortest path to the finish
##



def connectedEntranceCheck(maze, startingCoords):

    '''
    Takes a maze and a coordinate pair as parameters.
    Checks if the coordinate is connected to the entrance of the maze.
    Returns a version of the maze with 2s for connected points and 4s for non connected points,
    to make running quicker for subsequent points.
    Also returns a boolean that states whether the given point is connected to the entrance.
    '''

    # list which holds the IDs of all active node objects
    activeNodes = []

    
    # temporary list that is used when creating new active node objects
    # needed so that the new active nodes are not considered until next iteration
    newActiveNodes = []
    

    # create an active node at the starting point specified by the parameter
    newNode = ActiveNode(startingCoords[0], startingCoords[1], False)
    activeNodes.append(newNode)


    connected = False    # not yet known if node is connected to start of maze
    

    run = True
    
    while run == True:

        # if run out of activeNodes without finding the entrance, point is not connected
        # mark unconnected pixels with a 4
        
        if activeNodes == []:
            for x, y in np.argwhere(maze == 3):
                maze[x][y] = 4
                
            run = False


        else:
            
            for node in activeNodes:

                # each active node explores the area around it
                # it marks its current location with a 3,
                # before using findNewNodes function to find adjacent valid movements


                # marking path taken happens when active node is added to list
                maze[node.XValue, node.YValue] = 3  



                # find valid spaces to move to
                
                validMovements, connected, _ = node.findNewNodes(maze)



                # if entrance found, we know that all points currently marked as 3 are connected
                # mark connected points with a 2

                if connected == True:
                    for x, y in np.argwhere(maze == 3):
                        maze[x][y] = 2

                    run = False


                else:
                    
                    # move from one node to another
                    # add all nodes that are in validMovements list to newActiveNode list
                    
                    for coordPair in validMovements:
                        newNode = ActiveNode(coordPair[0], coordPair[1], node)
                        newActiveNodes.append(newNode)



            # now that we are done iterating through the activeNodes list,
            # we can clear it of all current nodes and add the next lot

            # remove all items from activeNodes

            activeNodes = []


                
            # add items from newActiveNodes to activeNodes
            
            for item in newActiveNodes:
                activeNodes.append(item)



            # clear newActiveNodes
            
            newActiveNodes = []

            

    return maze, connected







def drawMaze(window, maze, xCoord, yCoord, whiteBox = True):
    
    '''
    Parameters are window to draw maze on, maze itself and coordinates where top left corner should go
    Draws a white rectangle behind the maze, then draws a coloured square for each number in the maze array
    '''


    if whiteBox == True:
        # get width and height of maze for white rectangle
        # times both by 10, as each unit in the maze represents 10 pixels squared


        # len of the maze returns the number of columns
        mazeHeight = len(maze)*10


        # maze should be square, so each column has the same number of pixels in it
        # find the number of pixels in the first column, add 10 to mazeWidth for each and then break
        
        mazeWidth = 0
        
        for column in maze: 
            for item in column:
                mazeWidth += 10   # add 10 pixels to width
                
            break    # break, as all subsequent columns will have the same number of pixels


        # draw white rectangle to make sure maze doesn't clash with existing graphics
        
        pygame.draw.rect(window, WHITE, (xCoord, yCoord, mazeWidth, mazeHeight))



    #draw a black pixels for walls
    
    for y, x in np.argwhere(maze == 1):
        pygame.draw.rect(window, BLACK, (x*10 + xCoord, y*10 + yCoord, 10, 10))


    # draw green pixel at start

    for y, x in np.argwhere(maze == 9):
        pygame.draw.rect(window, GREEN, (x*10 + xCoord, y*10 + yCoord, 10, 10))


    # draw red pixel at finish

    for y, x in np.argwhere(maze == 8):
        pygame.draw.rect(window, RED, (x*10 + xCoord, y*10 + yCoord, 10, 10))


    # draw red pixels along shortest path

    for y, x in np.argwhere(maze == 7):
        pygame.draw.rect(window, RED, (x*10 + xCoord, y*10 + yCoord, 10, 10))




   

    



def eliminateDiagonals(maze):
    '''
    Each square of wall in the maze checks if the square to the top right
    or the square to the bottom right is purely diagonally connected to it.
    If this is found to be the case, it adds a wall immediately to the right of itself.
    '''
    
    for y, x in np.argwhere(maze == 1):
        try:
            
            # square to the upper right is purely diagonally connected
            if maze[y-1][x+1] == 1 and maze[y][x+1] == 0 and maze[y-1][x] == 0:    

                    # set square immediately to the right to a 1
                    maze[y][x+1] = 1


            # square to the lower right is purely diagonally connected
            if maze[y+1][x+1] == 1 and maze[y][x+1] == 0 and maze[y+1][x] == 0:    

                    # set square immediately to the right to a 1
                    maze[y][x+1] = 1   


        except IndexError:
            pass    # index error expected at the end of each row

    return maze



def eliminateTwoBlockWalls(maze, mazeWidth, mazeHeight):
    '''
    Takes maze as argument and returns it
    For each 2x2 block of wall, set the bottom right pixel to corridor
    '''
    

    for y, x in np.argwhere(maze == 1):

        if x > 0 and y > 0:
  
            # if not out of bounds and pixel to the right = 1
            # and pixel below = 1 and pixel to the right and below = 1
            
            if y+1 < mazeHeight and x+1 < mazeWidth and maze[y][x+1] == 1 \
               and maze[y+1][x] == 1 and maze[y+1][x+1] == 1:
                
                # set pixel to the right and below to 0
                maze[y+1][x+1] = 0
                
           
    return maze



def eliminateTwoBlockCorridors(maze, mazeWidth, mazeHeight):
    '''
    Takes maze as argument and returns it
    For each 2x2 block of corridor, set the bottom right pixel to wall
    '''

   
    for y, x in np.argwhere(maze == 0):

        # if not out of bounds and pixel to the right = 0
        # and pixel below = 0 and pixel to the right and below = 0
        
        if y+1 < mazeHeight and x+1 < mazeWidth and maze[y][x+1] == 0 \
            and maze[y+1][x] == 0 and maze[y+1][x+1] == 0:

            
            choice = random.randint(1, 2)
            
            if choice == 1:    
                # set pixel to the lower right to 1
                maze[y+1][x+1] = 1

            elif choice == 2:
                # set pixel (upper left of 2x2) to 1
                maze[y][x] = 1
        
    return maze






def removeSinglePixels(maze):
    '''
    Takes maze as argument and returns it
    For each wall in the maze that has no other walls orthogonaly adjacent, add a wall.
    '''
    
    for y, x in np.argwhere(maze == 1):

        try:
            
            # if pixel to the right = 0 and pixel below = 0
            # and pixel to the left = 0 and pixel above = 0
            
            if maze[y][x+1] == 0 and maze[y+1][x] == 0 \
               and maze[y][x-1] == 0 and maze[y-1][x] == 0:

                # set pixel above to 1
                maze[y-1][x] = 1
                
   
        except IndexError:
            pass    # index error expected at the end of each row

    return maze




def removeLongCorridors(maze):
    for y, x in np.argwhere(maze == 0):
        try:
            
            # if 6 0s in a row in the maze horizontally, set the rightmost to a 1
            if maze[y][x+1] == 0 and maze[y][x+2] == 0 and maze[y][x+3] == 0 and maze[y][x+4] == 0 and maze[y][x+5] == 0: #and maze[x+6][y] == 0:
                maze[y][x+5] = 1

        except IndexError:
            pass

    for y, x in np.argwhere(maze == 0):
        try:
            # if 5 0s in a row vertically, set the bottom 0 to a 1
            if maze[y+1][x] == 0 and maze[y+2][x] == 0 and maze[y+3][x] == 0 and maze[y+4][x] == 0 and maze[y+5][x] == 0:
                maze[y+5][x] = 1

        except IndexError:
            pass        
    

    return maze
        




def openContainedSpace(maze, mazeWidth, mazeHeight):
    '''For each unmarked space in the maze, checks if a path exists to the maze entrance'''


    shadowMaze = maze.copy()
    
    for x, y in np.argwhere(maze == 0):
        shadowMaze, connected = connectedEntranceCheck(shadowMaze, [x, y])


        if connected == False:
            
            blockToLose = random.randint(1, 4)
            if x+1 < mazeHeight and blockToLose == 1 and maze[x+1][y] == 1:
                maze[x+1][y] = 0
            elif y+1 < mazeWidth and blockToLose == 2 and maze[x][y+1] == 1:
                maze[x][y+1] = 0
            elif x-1 > -1 and blockToLose == 3 and maze[x-1][y] == 1:
                maze[x-1][y] = 0
            elif y-1 > -1 and blockToLose == 4 and maze[x][y-1] == 1:
                maze[x][y-1] = 0

    
    return maze

    

    


def main(mazeWidth, mazeHeight, window, xCoord, yCoord):

    '''
    Takes width and height of maze, window to draw maze on
    and x,y coordinates of maze's top left corner as parameters.
    Generates a maze, drawing the maze to the specified window
    after each iteration of the generating process.
    Returns matrix representing maze
    '''


    # generate a matrix of specified width and height, entirely consisting of '-1's
    # these will be replaced shortly
    
    mazeMatrix = np.array([[-1 for x in range(mazeWidth)] for y in range(mazeHeight)])


    # replace all '-1's with a randomly generated 1 or 0

    for y, x in np.argwhere(mazeMatrix == -1):
        mazeMatrix[y][x] = random.randint(0, 1)


    # stores the previous iteration of the maze, to later check if it is equal to the current iteration
    lastMaze = []


    run = True

    while run == True:
                            
        drawMaze(window, mazeMatrix, xCoord, yCoord)
        pygame.display.update()

                                                  
        mazeMatrix = openContainedSpace(mazeMatrix, mazeWidth, mazeHeight)
        
        mazeMatrix = eliminateTwoBlockCorridors(mazeMatrix, mazeWidth, mazeHeight)
        
        mazeMatrix = eliminateTwoBlockWalls(mazeMatrix, mazeWidth, mazeHeight)

        mazeMatrix = eliminateDiagonals(mazeMatrix)

        mazeMatrix = removeSinglePixels(mazeMatrix)



        # add in entrance, exit and outer walls

        for i in range(0, mazeWidth):
            mazeMatrix[0][i] = 1
            mazeMatrix[mazeHeight-1][i] = 1
        for i in range(0, mazeHeight):
            mazeMatrix[i][0] = 1
            mazeMatrix[i][mazeWidth-1] = 1

        mazeMatrix[0][1] = 9
        mazeMatrix[mazeHeight-1][mazeWidth-2] = 8
        mazeMatrix[mazeHeight-2][mazeWidth-2] = 0
        mazeMatrix[mazeHeight-3][mazeWidth-2] = 0
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



        # stop running the generator if the maze has stopped changing and path exists from start to finish

        mazeCopy = mazeMatrix.copy()
        if np.array_equal(lastMaze, mazeMatrix):

            
            _, connected = connectedEntranceCheck(mazeCopy, [mazeHeight-2, mazeWidth-2])

            
            if connected == True:
                run = False

        lastMaze = mazeMatrix.copy()



    return mazeMatrix

