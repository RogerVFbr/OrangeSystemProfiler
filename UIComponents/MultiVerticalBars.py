import pygame
from statistics import mean
import copy
from Resources.Colors import Colors as cl


class MultiVerticalBars:

    __TAG = 'MultiVerticalBars: '
    __multiVerticalBarsHistory = {}

    @classmethod
    def draw(cls,
             id,
             window,
             averaging = 60,
             positionAndSize = (0, 0, 0, 0),
             frameColor = (0, 0, 0),
             padding = 5,
             percentageList = [],
             caption = 'Core '
             ):

        noOfElements = len(percentageList)

        # ---> Initiate and update multiVerticalBarsHistory under provided ID
        if not id in cls.__multiVerticalBarsHistory:
            cls.__multiVerticalBarsHistory[id] = []

        elif len(cls.__multiVerticalBarsHistory[id])>=averaging:
            del cls.__multiVerticalBarsHistory[id][0]

        if percentageList != '':
            cls.__multiVerticalBarsHistory[id].append(percentageList)

        # ---> Calculate averages and reassign percentageList
        percentageList = []

        for x in range(noOfElements):
            averagesList = [(z[x]) for z in cls.__multiVerticalBarsHistory[id]]
            percentageList.append(round(mean(averagesList), 1))

        pygame.draw.rect(window, frameColor, positionAndSize)

        # ---> Inner Frame
        innerFrameRect = pygame.Rect(positionAndSize)
        innerFrameRect.topleft = (innerFrameRect.left+padding, innerFrameRect.top+padding)
        innerFrameRect.width -= padding*2
        innerFrameRect.height -= padding*2
        pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 10), innerFrameRect)

        zoneRect = copy.deepcopy(innerFrameRect)

        for x in range(noOfElements):

            # ---> Zones
            zoneRect.topleft = (int(round(innerFrameRect.left+(innerFrameRect.width/noOfElements)*x)), innerFrameRect.top)
            zoneRect.width = int(round((innerFrameRect.width/noOfElements)))
            pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 15), zoneRect, 1)

            # ---> Bar Labels
            font = pygame.font.Font(None, 20)
            text = font.render(caption + str(x+1), 1, (255,255,255))
            textRect = text.get_rect()
            textRect.topleft = (zoneRect.left+zoneRect.width/2-textRect.width/2, zoneRect.top+zoneRect.height-textRect.height-8)
            window.blit(text, textRect)

            # ---> Dividers
            marginFromZone = 10
            dividerRect = pygame.Rect(0, 0, 0, 0)
            dividerRect.topleft = (zoneRect.left+marginFromZone, zoneRect.top+zoneRect.height-textRect.height-20)
            dividerRect.height = 5
            dividerRect.width = zoneRect.width-marginFromZone*2
            pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 30), dividerRect)

            # ---> Full Bars
            marginFromZoneTop = 15
            fullBarRect = pygame.Rect(0, 0, 0, 0)
            fullBarRect.height = zoneRect.height-textRect.height-20-marginFromZoneTop
            fullBarRect.width = int(round((zoneRect.width-marginFromZone*2)*0.8))
            fullBarRect.topleft = (zoneRect.left+zoneRect.width/2-fullBarRect.width/2, zoneRect.top+marginFromZoneTop)
            pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 30), fullBarRect)

            # ---> Percentage Bars
            marginFromZoneTop = 20
            marginFromFullBarRect = 5
            percentBarRect = pygame.Rect(0, 0, 0, 0)
            percentBarRect.height = (zoneRect.height - textRect.height - 20 - marginFromZoneTop)
            percentBarRect.height = int(round(percentBarRect.height*percentageList[x]/100))
            percentBarRect.width = int(round((zoneRect.width - marginFromZone * 2) * 0.8)) - marginFromFullBarRect*2
            percentBarRect.topleft = ((zoneRect.left + zoneRect.width / 2 - fullBarRect.width / 2)+marginFromFullBarRect,
                                      zoneRect.top + marginFromZoneTop+(fullBarRect.height-percentBarRect.height)-marginFromFullBarRect)
            pygame.draw.rect(window, cl.alterColorBrightness(frameColor, -30), percentBarRect)

            # ---> Percentage index
            marginFromPercentBarTop = 5
            font = pygame.font.Font(None, 13)
            text = font.render(str(percentageList[x]) + '%', 1, (255, 255, 255))
            textRect = text.get_rect()
            textRect.topleft = (percentBarRect.left + percentBarRect.width/2 - textRect.width/2, percentBarRect.top+marginFromPercentBarTop)
            if textRect.top+textRect.height+3>fullBarRect.top+fullBarRect.height:
                textRect.top = fullBarRect.top+fullBarRect.height-textRect.height-3
            window.blit(text, textRect)