import numpy as np, pygame, sys # import libraries

pygame.init()


# array representing maze
# 9 marks start, 8 marks end, 1s are walls and 0s are empty space
# previously processed nodes will be marked by 3
# shortest path marked by 7


# define colours

WHITE = [255, 255, 255]
BLACK = [  0,   0,   0]
BLUE  = [  0,   0, 255]
RED   = [255,   0,   0]
GREEN = [  0, 255,   0]



class ActiveNode():
    
    def __init__(self, XValue, YValue, parentNode):
        '''
        Initialise each instance of node object
        Takes parameters XValue, YValue and parentNode
        XValue and YValue refer to the node's position in the maze
        parentNode is the node that the node originated from
        parentNode = False for the starting node in the maze
        '''
       
        self.XValue = XValue
        self.YValue = YValue
        self.parentNode = parentNode



    def findNewNodes(self, maze):
        '''
        Given a node in the maze, find adjacent nodes that can be moved to.
        Returns a list of all valid movements,
        as well as a boolean that holds whether the exit has been found.
        '''
    
        # locate an adjacent space to move to
        # start by looking at all possible movements
 
        possibleMovements = [[self.XValue - 1, self.YValue], [self.XValue + 1, self.YValue]\
                             , [self.XValue, self.YValue - 1], [self.XValue, self.YValue + 1]]
        validMovements = []


        foundExit = False   # not yet found the exit to the maze
        foundStart = False   # not yet found the start of the maze



        
        for row, column in possibleMovements:
            try:

                if maze[row][column] == 8:
                    foundExit = True    # found finish!

                elif maze[row][column] == 9:
                    foundStart = True

                elif maze[row][column] == 2:
                    foundStart = True    # spaces connected to the start are marked with a 2

                elif maze[row][column] == 0:
                    validMovements.append([row, column])    # add each valid movement to a list
                    maze[row][column] = 3

            except IndexError: # index error expected when at the edge of the maze
                pass


        return validMovements, foundStart, foundExit
        


def getWidth(maze):
    '''
    Returns the width of a maze in pixels - every unit of the maze is 10 pixels
    '''
    
    width = 0
    for i in maze[0]:
        width += 10
    return width



def getHeight(maze):
    '''
    Returns the height of a maze in pixels - every unit of the maze is 10 pixels
    '''

    height = len(maze)*10
    
    return height



def findStart(maze):

    # First, find the start of the maze - marked by a 9
    # numStarts variable holds how many 9s have been found
    
    numStarts = 0

    for row, column in np.argwhere(maze == 9):
        numStarts += 1
        startNode = [row+1, column]
    

    # cannot have more than one starting point
    # if numStarts is >1, maze is invalid

    if numStarts > 1:
        print("Error - maze has too many entrances")

    return startNode



# main solving loop

def main(maze):

    startingCoords = findStart(maze)


    # list which holds the IDs of all active node objects
    activeNodes = []

    # temporary list that is used when creating new active node objects
    newActiveNodes = []


    # get the starting node of the maze
    
    newNode = ActiveNode(startingCoords[0], startingCoords[1], False)
    activeNodes.append(newNode)
    

    run = True
    
    while run == True:
        for node in activeNodes:
            
            # mark path taken
            
            maze[node.XValue, node.YValue] = 3


            # find valid spaces to move to
            
            validMovements, _, foundExit = node.findNewNodes(maze)


            # if exit has been found, we can stop exploring the maze
            # and start looking for the shortest path

            if foundExit == True:
                run = False
                return node

            
            # move from one space to another
            # add all spaces that are in validMovements list to newActiveNode list
            
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


        # allows the user to quit the window while the program is running
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



# trace back the path from the node that finished first

def findRoute(finishNode, maze, window):
    run = True
    finishPath = []

    while run == True:

        # add the current node to the path taken
        # then, find the node that that node originated from and repeat
        
        finishPath.append(finishNode)
        finishNode = finishNode.parentNode


        # when the parent node = False, reached the start of the maze
        
        if finishNode == False:
            run = False

        
    # get rid of all the 3s in the maze so that just the finish path is shown

    for x, y in np.argwhere(maze == 3):
        maze[x][y] = 0
        


    return maze, finishPath
        





