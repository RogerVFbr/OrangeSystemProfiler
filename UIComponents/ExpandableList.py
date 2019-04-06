import pygame
from Resources.Colors import Colors as cl


class ExpandableList:

    @classmethod
    def draw(cls,
             window,                           # Reference surface
             positionAndSize = (0, 0, 0, 0),   # Position and size tuple
             dataBGExtension = 100,            # Value data display size
             margins = (7, 5),                 # Margins between cells
             title = '',                       # Title
             titleAlignment = 'center',        # Title alignment
             data = {},                        # Data to be displayed
             captionBGColor = (60, 60, 60),    # Keys (or 'caption') background color
             valueBGColor = (200, 200, 200),   # Value background color
             textBrightness = (100, 100),      # Color contrast text/background
             fontSize = 18):                   # Font size

        position = pygame.Rect(positionAndSize)

        for x, key in enumerate(data):

            marginBetweenLines = 0 if x is 0 else margins[1]

            # ---> Draw value BG
            position = pygame.Rect(positionAndSize)
            position.topleft = (position.top,
                                position.left + (positionAndSize[3] + marginBetweenLines) * x)
            position.width = dataBGExtension
            pygame.draw.rect(window, valueBGColor, position)

            # ---> Draw caption
            position = pygame.Rect(positionAndSize)
            font = pygame.font.Font(None, fontSize)
            text = font.render(str(data[key]), 1, cl.alterColorBrightness(valueBGColor, textBrightness[1]))
            textRect = text.get_rect()
            textRect.topleft = (position.top + position.width+5,
                                position.left + (positionAndSize[3] + marginBetweenLines) * x +
                                positionAndSize[3] / 2 - textRect.height / 2 + 1)
            window.blit(text, textRect)

            # ---> Draw caption BG
            position = pygame.Rect(positionAndSize)
            position.topleft = (position.top+1,
                                         position.left+(positionAndSize[3]+marginBetweenLines)*x+1)
            position.width -= 2
            position.height -= 2
            pygame.draw.rect(window, captionBGColor, position)

            # ---> Draw caption
            position = pygame.Rect(positionAndSize)
            font = pygame.font.Font(None, fontSize)
            text = font.render(key, 1, cl.alterColorBrightness(captionBGColor, textBrightness[0]))
            textRect = text.get_rect()
            textRect.topleft = (position.top+positionAndSize[2]/2-textRect.width/2,
                                position.left+(positionAndSize[3]+marginBetweenLines)*x+
                                positionAndSize[3]/2-textRect.height/2+1)
            window.blit(text, textRect)

        # ---> Draws list title
        font = pygame.font.Font(None, 25)
        text = font.render(title, 1, (220, 220, 220))
        textRect = text.get_rect()

        if titleAlignment is 'left':
            textRect.topleft = (position.top,
                                position.left-position.height+5)

        elif titleAlignment is 'center':
            textRect.topleft = (position.top+dataBGExtension/2-textRect.width/2,
                                position.left - position.height + 5)

        window.blit(text, textRect)