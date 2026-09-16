# TODO
# generation fails sometimes - just keeps going indefinitely
# make a main function
# add comments


# import modules, as well as maze generator and solver

import pygame, sys, numpy as np
import Amazeing_Maze_Generator as mazeGenerator
import Maze_Solving as mazeSolver
import Slider_Class as slider



pygame.init()


# define colours, font and window

WHITE  = [255, 255, 255]
BLACK  = [  0,   0,   0]
YELLOW = [255, 221,  51]
RED    = [255,   0,   0]
BLUE   = [  0,   0, 255]




# set up window

windowWidth = 1200
windowHeight = 700

window = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
pygame.display.set_caption("Amazeing Maze Generator")




class Stack():
    def __init__(self): # initialise the stack and the location of the top pointer
        self.stack = []
        self.topOfStackPointer = -1

    def __str__(self): # return the contents of the stack if it is printed
        return str(self.stack)

    def push(self, item): # add an item to the stack and increment the top pointer
        self.stack.append(item)
        self.topOfStackPointer += 1

    def pop(self): # remove the item closest to the top of the stack and return it
                   # also decrease top of stack pointer by 1
        if self.topOfStackPointer > -1:

            data = self.stack[self.topOfStackPointer]
            del self.stack[-1]
            self.topOfStackPointer -= 1

        else: # if the stack pointer = -1, the stack is empty
            print("No item to pop")
            data = False
            
        return data


    def peek(self): # return the item at the top of the stack without removing it
        if self.topOfStackPointer > -1:
            data = self.stack[self.topOfStackPointer]
        else:
            data = False # if stack empty, return false

        return data




def drawText(text, XCenter, YCenter, small = False):
    '''Input text, X coordinate and Y coordinate, draw text to screen with inputted center.
        'small' parameter defaults to false, but allows for a smaller font size when set to true.'
        Returns the textbox.'''


    if small == True: # set fontsize based on small parameter
        font = pygame.font.SysFont("freesansbold", 36)

    else:
        font = pygame.font.SysFont("freesansbold", 50)


    textSurface = font.render(str(text), True, BLACK, WHITE)

    # create a rectangle containing the text box
    textRectangle = textSurface.get_rect()

    # set the center of the rectangle to the desired coordinate
    textRectangle.center = (XCenter, YCenter)


    # draw the text to the screen at the loctation of the rectangle
    window.blit(textSurface, textRectangle)

    return textRectangle


def getWidthHeight(maze):

    '''
    Takes maze as input.
    Returns width and height of maze.
    '''

    
    # len of the maze returns the number of rows
    mazeHeight = len(maze)


    # maze should be square, so each row has the same number of pixels in it
    
    mazeWidth = 0
    
    for row in maze: 
        for item in row:
            mazeWidth += 1   # add 1 pixels to width
            
        break    # break, as all subsequent rows will have the same number of pixels

    return mazeWidth, mazeHeight








def drawButtons():
    '''
    Draws the top row of buttons to the screen.
    Changes colour of buttons when mouse is hovering over them.
    Returns a list of 4 rectangles representing the buttons.
    '''

    # write all the labels on the buttons

    drawText("Menu ->", 200, 50)
    drawText("Generate", 500, 28)
    drawText("Maze", 500, 70)
    drawText("Solve", 700, 28)
    drawText("Maze", 700, 70)
    drawText("Explore", 900, 28)
    drawText("Maze", 900, 70)
    drawText("Saved", 1100, 28)
    drawText("Mazes", 1100, 70)

    
    # draw black box around 'menu' label
    # don't need the rectangle, as isn't a pressable button
    pygame.draw.rect(window, BLACK, (0, 0, 400, 100), 10)


    # rectangle around 'generate maze' label
    drawMazeRect    = pygame.draw.rect(window, BLACK, (400, 0, 200, 100), 10)

    # 'solve maze'
    solveMazeRect   = pygame.draw.rect(window, BLACK, (600, 0, 200, 100), 10)

    # 'explore maze'
    exploreMazeRect = pygame.draw.rect(window, BLACK, (800, 0, 200, 100), 10)

    # 'saved mazes'
    fileRect        = pygame.draw.rect(window, BLACK, (1000, 0, 200, 100), 10)


    # list of the rectangles just created
    rectList = [drawMazeRect, solveMazeRect, exploreMazeRect, fileRect]


    # check if the mouse collides with any of the buttons
    # if it does, draw a yellow rectangle over the top
    for rect in rectList:
        if rect.collidepoint(mouseX, mouseY) == True:
            pygame.draw.rect(window, YELLOW, (rect), 10)

    return rectList




def updateMaze():

    # centres the maze on the screen using screen width and height, as well as maze width and height
    mazeGenerator.drawMaze(window, maze, ((windowWidth-(mazeWidth*10))//2), (((windowHeight + 100) - (mazeHeight*10))//2), False)





def drawGenerationOptionsWindow(window, mouseX, mouseY, clicked):
    pygame.draw.rect(window, WHITE, (400, 90, 200, 350))
    pygame.draw.rect(window, BLACK, (400, 90, 200, 350), 10)

    heightSlider.handleSlider(window, mouseX, mouseY, clicked)
    widthSlider.handleSlider(window, mouseX, mouseY, clicked)




def drawSavedMazeWindow(window, mouseX, mouseY, saveSlotChoice):

    # draw a white box with a black border to make up the window
    pygame.draw.rect(window, WHITE, (1000, 90, 200, 350))
    pygame.draw.rect(window, BLACK, (1000, 90, 200, 350), 10)

    # draw the three buttons in the window, and get their rect objects
    maze1Button = pygame.draw.rect(window, BLACK, (1030, 130, 140, 60), 7)
    maze2Button = pygame.draw.rect(window, BLACK, (1030, 230, 140, 60), 7)
    maze3Button = pygame.draw.rect(window, BLACK, (1030, 330, 140, 60), 7)


    # draw yellow rectangles around the buttons if they are being hovered over
    if maze1Button.collidepoint(mouseX, mouseY):
        pygame.draw.rect(window, YELLOW, (1030, 130, 140, 60), 7)

    elif maze2Button.collidepoint(mouseX, mouseY):
        pygame.draw.rect(window, YELLOW, (1030, 230, 140, 60), 7)

    elif maze3Button.collidepoint(mouseX, mouseY):
        pygame.draw.rect(window, YELLOW, (1030, 330, 140, 60), 7)


    # when no slot selected, give the user the choice of all 3 slots
    # draw according text
    if saveSlotChoice == False:
        drawText("Maze 1", 1100, 160, True)
        drawText("Maze 2", 1100, 260, True)
        drawText("Maze 3", 1100, 360, True)


    else:

        # when a slot is selected, display the slot number on first button
        # then 'save' and 'load' on 2 lower buttons
        drawText(str("Maze " + str(saveSlotChoice)), 1100, 160, True)
        drawText("Save", 1100, 260, True)
        drawText("Load", 1100, 360, True)
        pygame.draw.rect(window, BLUE, (1030, 130, 140, 60), 7)


    return maze1Button, maze2Button, maze3Button





def updateWindow(fillWhite, buttonUpdate, mazeUpdate, optionsWindow, savedMazeWindow, mouseX,\
mouseY, clicked, solveMaze, exploreMaze, exploreCoords, pastExploreList, mazeTopLeft, saveSlotChoice):

    if fillWhite == True:

        # completely fill the screen with white
        window.fill(WHITE)





    if exploreMaze == True:

        # draw in blue the nodes user has visited in the past
        for coordinates in pastExploreList:
            pygame.draw.rect(window, BLUE, (mazeTopLeft[0] + \
                coordinates[0]*10, mazeTopLeft[1] + coordinates[1]*10, 10, 10))

        # draw in red the user's current location
        pygame.draw.rect(window, RED, (mazeTopLeft[0] + \
                exploreCoords[0]*10, mazeTopLeft[1] + exploreCoords[1]*10, 10, 10))


    if mazeCreated == True and mazeUpdate == True:

        # redraw the maze to the screen
        updateMaze()

        

    if optionsWindow == True:

        # draw the options window under generate maze button
        drawGenerationOptionsWindow(window, mouseX, mouseY, clicked)


    if savedMazeWindow == True:

        # draw options window under saved mazes button, returns rectangles for the three mini buttons
        maze1Button, maze2Button, maze3Button = drawSavedMazeWindow(window, mouseX, mouseY, saveSlotChoice)

    else:

        # buttons still have to exist if the window isn't open, so just make them unclickable
        maze1Button = pygame.Rect(0, 0, 0, 0)
        maze2Button = pygame.Rect(0, 0, 0, 0)
        maze3Button = pygame.Rect(0, 0, 0, 0)


    if buttonUpdate == True:

        # draw the buttons to the screen and get a list of their rectangles
        rectList = drawButtons()


    if exploreMaze == True:

        # draw blue rectangle around explore maze button if it is active
        pygame.draw.rect(window, BLUE, (800, 0, 200, 100), 10)


    if solveMaze == True:

        # draw blue rectangle around solve maze button if it is active
        pygame.draw.rect(window, BLUE, (600, 0, 200, 100), 10)


    pygame.display.update()

    return rectList, maze1Button, maze2Button, maze3Button




def handleUserExploration(maze, exploreCoords, pastExploreList, exploreDirectionStack):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # user tries to move upwards

                # move is valid
                if maze[exploreCoords[1]-1][exploreCoords[0]] != 1 and exploreCoords[1]-1 >= 1:

                    # if last movement was down, undo previous move
                    if exploreDirectionStack.peek() == "down":
                        exploreDirectionStack.pop()

                        exploreCoords = [exploreCoords[0], exploreCoords[1]-1]
                        pastExploreList.remove(exploreCoords)

                    # else, add new movement to stack and change exploreCoords
                    else:
                        pastExploreList.append(exploreCoords)
                        exploreDirectionStack.push("up")

                        exploreCoords = [exploreCoords[0], exploreCoords[1]-1]



            if event.key == pygame.K_DOWN:
                # user tries to move downwards

                # move is valid
                if maze[exploreCoords[1]+1][exploreCoords[0]] != 1 and exploreCoords[1]+2 < mazeHeight:

                    # if last movement was up, undo previous move
                    if exploreDirectionStack.peek() == "up":
                        exploreDirectionStack.pop()

                        exploreCoords = [exploreCoords[0], exploreCoords[1]+1]
                        pastExploreList.remove(exploreCoords)

                    # else, add new movement to stack and change exploreCoords
                    else:
                        pastExploreList.append(exploreCoords)
                        exploreDirectionStack.push("down")

                        exploreCoords = [exploreCoords[0], exploreCoords[1]+1]



            if event.key == pygame.K_LEFT:
                # user tries to move left

                if maze[exploreCoords[1]][exploreCoords[0]-1] != 1: # move is valid

                    # if last movement was right, undo previous move
                    if exploreDirectionStack.peek() == "right":
                        exploreDirectionStack.pop()

                        exploreCoords = [exploreCoords[0]-1, exploreCoords[1]]
                        pastExploreList.remove(exploreCoords)

                    # else, add new movement to stack and change exploreCoords
                    else:
                        pastExploreList.append(exploreCoords)
                        exploreDirectionStack.push("left")

                        exploreCoords = [exploreCoords[0]-1, exploreCoords[1]]



            if event.key == pygame.K_RIGHT:
                # user tries to move right

                if maze[exploreCoords[1]][exploreCoords[0]+1] != 1: # move is valid

                    # if last movement was left, undo previous move
                    if exploreDirectionStack.peek() == "left":
                        exploreDirectionStack.pop()

                        exploreCoords = [exploreCoords[0]+1, exploreCoords[1]]
                        pastExploreList.remove(exploreCoords)

                    # else, add new movement to stack and change exploreCoords
                    else:
                        pastExploreList.append(exploreCoords)
                        exploreDirectionStack.push("right")

                        exploreCoords = [exploreCoords[0]+1, exploreCoords[1]]



        return maze, exploreCoords, pastExploreList, exploreDirectionStack









def cleanMaze(maze):
    for y, x in np.argwhere(maze):

        if maze[y][x] == 0 or maze[y][x] == 1 or maze[y][x] == 9 or maze[y][x] == 8:
            pass
        else:
            maze[y][x] = 0

    return maze






mouseX = windowWidth //2
mouseY = windowHeight //2

mazeWidth = 60
mazeHeight = 60

mazeCreated = False
mazeTopLeft = [0, 1]

exploreMaze = False
exploreCoords = [0, 0]
pastExploreList = []
exploreDirectionStack = Stack()

solveMaze = False

clicked = False

mouseX, mouseY = [0, 0]

widthSlider = slider.Slider(415, 150, 10, 120, "Width")
heightSlider = slider.Slider(415, 300, 10, 60, "Height")

optionsWindow = False
saveSlotChoice = False

savedMazeWindow = False

run = True
while run == True:

    rectList, maze1Button, maze2Button, maze3Button = updateWindow(True, True, True, \
        optionsWindow, savedMazeWindow, mouseX, mouseY, clicked, solveMaze, exploreMaze,\
        exploreCoords, pastExploreList, mazeTopLeft, saveSlotChoice)


    for event in pygame.event.get():

        if exploreMaze == True:
            maze, exploreCoords, pastExploreList, exploreDirectionStack = \
                  handleUserExploration(maze, exploreCoords, pastExploreList, exploreDirectionStack)

        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False




        if clicked == True:
            
            if rectList[0].collidepoint(mouseX, mouseY) == True:
                
                mouseX, mouseY = 0, 0    # stops accidental double clicking
                
                optionsWindow = False
                clicked = False

                # clear maze area
                pygame.draw.rect(window, WHITE, (0, 100, windowWidth, windowHeight -100))

                # draw blue rectangle around generate maze button
                pygame.draw.rect(window, BLUE, (400, 0, 200, 100), 10)

                # get rid of blue rect around solve maze button
                pygame.draw.rect(window, BLACK, (600, 0, 200, 100), 10)

                # get rid of blue rect around explore maze button
                pygame.draw.rect(window, BLACK, (800, 0, 200, 100), 10)

                exploreMaze = False
                solveMaze = False


                # get width and height from sliders
                mazeWidth, mazeHeight = [widthSlider.currentValue, heightSlider.currentValue]

                # work out where to draw the maze from based on its width and height so that it is centred
                mazeTopLeft = [((windowWidth-(mazeWidth*10))//2), (((windowHeight + 100) - (mazeHeight*10))//2)]

                # actually generate maze
                maze = mazeGenerator.main(mazeWidth, mazeHeight, window, mazeTopLeft[0], mazeTopLeft[1])
                mazeCreated = True
                



            elif mazeCreated == True and rectList[1].collidepoint(mouseX, mouseY) == True:
                optionsWindow = False
                mouseX, mouseY = 0, 0    # stops accidental double clicking
                clicked = False
                solveMaze = not solveMaze

                if solveMaze == True:
                    pygame.draw.rect(window, BLUE, (600, 0, 200, 100), 10) # draw blue box over solve maze button

                    # actually call the solving algorithm and get shortest path
                    finishNode = mazeSolver.main(maze)
                    maze, finishPath = mazeSolver.findRoute(finishNode, maze, window)
                    

                    # reveal the shortest path one pixel at a time
                    for counter in range(len(finishPath)-1, -1, -1):
                        
                        maze[finishPath[counter].XValue][finishPath[counter].YValue] = 7
                        
                        updateMaze()
                        pygame.display.update()
                        pygame.time.Clock().tick(120)


                # if solveMaze now false, remove all 7s in the maze, hiding the shortest path
                else:
                    for y,x in np.argwhere(maze == 7):
                        maze[y][x] = 0


            elif mazeCreated == True and rectList[2].collidepoint(mouseX, mouseY) == True:

                exploreCoords = [1, 0]
                pastExploreList = []

                exploreMaze = not exploreMaze




            elif savedMazeWindow == True:

                # if top button pressed
                if maze1Button.collidepoint(mouseX, mouseY):
                    mouseX, mouseY = 1000, 200    # stops accidental double clicking
                    clicked = False

                    # if no slot selected, select slot 1
                    if saveSlotChoice == False:
                        saveSlotChoice = 1

                    else:
                        # if slot selected, go back to main menu
                        saveSlotChoice = False


                
                # if middle button pressed
                elif maze2Button.collidepoint(mouseX, mouseY):
                    mouseX, mouseY = 1000, 200    # stops accidental double clicking
                    clicked = False
                    
                    # if no slot selected, select slot 2
                    if saveSlotChoice == False:
                        saveSlotChoice = 2

                    # if save slot selected, button 2 is the save button
                    elif mazeCreated == True:

                        # save to slot 1
                        if saveSlotChoice == 1:
                            file = open("Saved_Maze_1.txt", "w")

                        # save to slot 2
                        elif saveSlotChoice == 2:
                            file = open("Saved_Maze_2.txt", "w")

                        # save to slot 3
                        elif saveSlotChoice == 3:
                            file = open("Saved_Maze_3.txt", "w")


                        # get rid of all 2s, 3s and 4s in the maze
                        mazeToSave = maze.copy()
                        mazeToSave = cleanMaze(mazeToSave)
                        
   
                        for line in mazeToSave:

                            # write each number in the line to file
                            for character in line:
                                file.write(str(character))

                            # start new line in file
                            file.write("\n")

                        # done writing, so close file
                        file.close()

                        
                # if bottom button pressed
                elif maze3Button.collidepoint(mouseX, mouseY):
                    mouseX, mouseY = 1000, 200    # stops accidental double clicking
                    clicked = False

                    # if no save slot selected, choose slot 3
                    if saveSlotChoice == False:
                        saveSlotChoice = 3
                        
                    # if save slot selected, button 3 is load maze button
                    else:

                        # load from slot 1
                        if saveSlotChoice == 1:
                            file = open("Saved_Maze_1.txt", "r")

                        # load from slot 2
                        elif saveSlotChoice == 2:
                            file = open("Saved_Maze_2.txt", "r")

                        # load from slot 3
                        elif saveSlotChoice == 3:
                            file = open("Saved_Maze_3.txt", "r")
                            

                            
                        # sort out some settings
                        mazeCreated = True
                        solveMaze = False
                        exploreMaze = False

                        # start with an empty maze
                        maze = []
                        

                        # lines in the file are a string of numbers, with no characters between
                        for line in file:

                            # list(line) returns a list of all the characters in the line
                            list1 = list(line)

                            # remove the newline character from the end of the list
                            list1.remove(list1[-1])

                            # cast each number from string to integer
                            for i in range(len(list1)):
                                list1[i] = int(list1[i])

                            # append the list to the maze
                            maze.append(list1)

                        # change maze data type to numpy.array
                        maze = np.array(maze)

                        # finished reading, so close file
                        file.close()
                        
                        # get data about maze to draw it to screen
                        mazeWidth, mazeHeight = getWidthHeight(maze)
                        mazeTopLeft = [((windowWidth-(mazeWidth*10))//2), \
                                       (((windowHeight + 100) - (mazeHeight*10))//2)]



              

                        




            elif mazeCreated == False:
                pass
                # TODO could put an arrow to the create maze button?










        # get rid of the generation options window when mouse over solve maze button
        if rectList[1].collidepoint(mouseX, mouseY) == True:
            optionsWindow = False

        # draw options window if mouse over draw maze button
        elif rectList[0].collidepoint(mouseX, mouseY):
            optionsWindow = True

        # if options window already showing, be more lenient about when to hide it
        elif optionsWindow == True and mouseX >= 300 and mouseX <= 700 and mouseY <= 440:
            optionsWindow = True

        else:
            optionsWindow = False




        # if window is closed, forget any choice the user made
        if savedMazeWindow == False:
            saveSlotChoice = False

        # get rid of save maze window when mouse over explore maze button
        if rectList[2].collidepoint(mouseX, mouseY):
            savedMazeWindow = False

        # show the window if the mouse is hovering over it
        if rectList[3].collidepoint(mouseX, mouseY):
            savedMazeWindow = True

        # if window already showing, be lenient on when to hide it
        elif savedMazeWindow == True and mouseX >= 900 and mouseY <= 440:
            savedMazeWindow = True

        else:
            savedMazeWindow = False




    pygame.time.Clock().tick(60)













