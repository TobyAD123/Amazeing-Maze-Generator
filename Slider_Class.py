import pygame, sys

pygame.init()


BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]
YELLOW =[255, 221,  51]

font = pygame.font.SysFont("freesansbold", 40)


def drawText(window, text, XCenter, YCenter):
    '''Input text, X coordinate and Y coordinate, draw text to screen with inputted center.
       Return the textbox, if it is needed.'''

    textSurface = font.render(str(text), True, BLACK, WHITE)
    textRectangle = textSurface.get_rect()
    textRectangle.center = (XCenter, YCenter)
    window.blit(textSurface, textRectangle)

    return textRectangle





class Slider():
    def __init__(self, XCoord, YCoord, lowerBound, upperBound, text):
        self.XCoord = XCoord
        self.YCoord = YCoord
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.currentValue = lowerBound
        self.sliderWidth = 150
        self.sliderHeight = 50
        self.text = text
        self.selected = False



    def drawSlider(self, window):

        # write whatever the user has named the slider,
        # followed by the slider's current value at a point centered above the slider
        drawText(window, (self.text + " : " + str(self.currentValue)),\
                 self.XCoord + self.sliderWidth//2 + 10, self.YCoord - 10)

        # get the X-Coordinate of the moveable part of the slider
        sliderXPosition = self.XCoord + ((self.currentValue-self.lowerBound)\
                /(self.upperBound-self.lowerBound))*self.sliderWidth

        # draw the slider bar
        pygame.draw.line(window, BLACK, (self.XCoord, self.YCoord + self.sliderHeight//2), \
                         (self.XCoord + self.sliderWidth - 1 + 20, self.YCoord + self.sliderHeight//2), 5)


        

        # if slider being moved, draw the movable part of the slider in a different colour
        if self.selected == True:
            sliderRect = pygame.draw.rect(window, YELLOW, (sliderXPosition, \
                    self.YCoord + self.sliderHeight//2 - 10, 20, 20), 5)

        else:
            # draw the movable part of the slider
            sliderRect = pygame.draw.rect(window, BLACK, (sliderXPosition, \
                    self.YCoord + self.sliderHeight//2 - 10, 20, 20), 5)


        # draw the little white box inside the movable part of the slider
        pygame.draw.rect(window, WHITE, (sliderXPosition+5, self.YCoord \
                + self.sliderHeight//2 - 5, 10, 10))


        return sliderRect, sliderXPosition



    def handleSlider(self, window, mouseX, mouseY, clicked):
        
        # call the drawslider function
        sliderRect, sliderXPosition = self.drawSlider(window)


        # if mouse button down and mouse over slider button, slider is selected
        if clicked == True:
            if sliderRect.collidepoint(mouseX, mouseY) == True:
                
                self.selected = True

        else:
            self.selected = False



        # if slider is selected and mouse is to the right of slider button:
        # increase number on slider, thus moving it right
        
        if self.selected == True and mouseX >= sliderXPosition:
            while mouseX > sliderXPosition + 10 and self.currentValue < self.upperBound:

                self.currentValue += 1

               

                # call drawSlider again to show the changes to the movable part
                sliderRect, sliderXPosition = self.drawSlider(window)


        # if slider is selected and mouse is to the left of slider button:
        # decrease number on slider, moving it left
        
        if self.selected == True and mouseX < sliderXPosition:
            while mouseX < sliderXPosition and self.currentValue > self.lowerBound:
                self.currentValue -= 1

                
                sliderRect, sliderXPosition = self.drawSlider(window)














