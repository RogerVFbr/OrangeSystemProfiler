import copy
import pygame
from Resources.Colors import Colors as cl
from pygame.locals import *


class ScrollableTable:

    __tableInfo = {}
    __mouseInfo = {
        'pointer': (0, 0),
        'isLeftButtonPressed': False,
        'isRightButtonPressed': False
    }
    
    @classmethod
    def draw(cls,
             id,
             window,
             positionAndSize = (10, 95, 780, 495),
             frameColor = (255, 255, 255),
             headerColor = (255, 255, 255),
             data = [],
             columnWeight = [],
             padding = 5):

        if len(columnWeight) is not len(data[0]): columnWeight = [1 for x in list(range(len(data[0])))]

        if id not in cls.__tableInfo or cls.__tableInfo[id]['rect'] != pygame.Rect(positionAndSize):
            cls.__tableInfo[id] = {
                'scrollBarY': None,
                'dataPositionModifier': 0,
                'rect': pygame.Rect((positionAndSize))
            }

        pygame.draw.rect(window, frameColor, positionAndSize)

        # ---> General variable definitions
        dataLineHeight = 20
        totalDataHeight = dataLineHeight * len(data) - 1
        headerHeight = 30
        headerMarginBottom = 5
        dataFrameHeight = positionAndSize[3] - padding * 2 - headerHeight - headerMarginBottom
        navigationRectHeight = 28
        navigationRectMargin = 2
        innerFrameHeight = positionAndSize[3] - padding * 2
        scrollBarFrameScrollableAreaHeight = innerFrameHeight - navigationRectHeight * 2 - navigationRectMargin * 4
        noOfColumns = len(data[0])

        scrollBarHeight = int(round((dataFrameHeight/totalDataHeight)*scrollBarFrameScrollableAreaHeight))
        scrollBarHeight = scrollBarHeight if scrollBarHeight<=scrollBarFrameScrollableAreaHeight else scrollBarFrameScrollableAreaHeight


        # ---> Inner Frame
        innerFrameRect = pygame.Rect(positionAndSize)
        innerFrameRect.topleft = (innerFrameRect.left + padding, innerFrameRect.top + padding)
        innerFrameRect.width -= padding * 2
        innerFrameRect.height = innerFrameHeight
        # pygame.draw.rect(window, Helpers.alterColorBrightness(frameColor, 10), innerFrameRect)

        # ---> Scrollbar frame
        scrollBarFrameRect = copy.deepcopy(innerFrameRect)
        scrollBarFrameRect.width = 20
        scrollBarFrameRect.topleft = (scrollBarFrameRect.left+innerFrameRect.width-scrollBarFrameRect.width,
                                      scrollBarFrameRect.top)
        pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 20), scrollBarFrameRect)

        # ---> Scrollbar navigation arrow top
        navigationTopRect = copy.deepcopy(scrollBarFrameRect)
        navigationTopRect.height = navigationRectHeight
        navigationTopRect.width -= navigationRectMargin*2
        navigationTopRect.topleft = (navigationTopRect.left+navigationRectMargin,
                                     navigationTopRect.top+navigationRectMargin)
        pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 30), navigationTopRect)
        pygame.draw.polygon(window, cl.alterColorBrightness(frameColor, 50),
                            (
                                (navigationTopRect.left+3, navigationTopRect.bottom-8),
                                (navigationTopRect.right-3, navigationTopRect.bottom-8),
                                (navigationTopRect.left+navigationTopRect.width/2, navigationTopRect.top+8),

                            ), 0)

        if cls.__mouseInfo['isLeftButtonPressed']:

            if navigationTopRect.collidepoint(cls.__mouseInfo['pointer']):

                cls.__tableInfo[id]['dataPositionModifier'] -= int(round(totalDataHeight/len(data)))
                cls.__tableInfo[id]['scrollBarY'] -= int(round(scrollBarFrameScrollableAreaHeight/len(data)))

                if cls.__tableInfo[id]['scrollBarY'] <= navigationTopRect.bottom+3:
                    cls.__tableInfo[id]['dataPositionModifier'] = 0
                    cls.__tableInfo[id]['scrollBarY'] = navigationTopRect.bottom+3


        # ---> Scrollbar navigation arrow bottom
        navigationBottomRect = copy.deepcopy(navigationTopRect)
        navigationBottomRect.topleft = (navigationBottomRect.left,
                                        scrollBarFrameRect.bottom - 2 - navigationBottomRect.height)
        pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 30), navigationBottomRect)
        pygame.draw.polygon(window, cl.alterColorBrightness(frameColor, 50),
                            (
                                (navigationBottomRect.left + 3, navigationBottomRect.top + 8),
                                (navigationBottomRect.right - 3, navigationBottomRect.top + 8),
                                (navigationBottomRect.left + navigationBottomRect.width / 2, navigationBottomRect.bottom - 8),

                            ), 0)

        if cls.__mouseInfo['isLeftButtonPressed']:

            if navigationBottomRect.collidepoint(cls.__mouseInfo['pointer']):

                cls.__tableInfo[id]['dataPositionModifier'] += int(round(totalDataHeight/len(data)))
                cls.__tableInfo[id]['scrollBarY'] += int(round(scrollBarFrameScrollableAreaHeight/len(data)))

                if cls.__tableInfo[id]['scrollBarY'] + scrollBarHeight >= \
                        navigationTopRect.bottom + 3 + scrollBarFrameScrollableAreaHeight:

                    cls.__tableInfo[id]['dataPositionModifier'] = int(round(((scrollBarFrameScrollableAreaHeight - scrollBarHeight)/scrollBarFrameScrollableAreaHeight)*totalDataHeight))
                    cls.__tableInfo[id]['scrollBarY'] = navigationTopRect.bottom + 3 + scrollBarFrameScrollableAreaHeight - scrollBarHeight

        # ---> Table frame
        tableRect = copy.deepcopy(innerFrameRect)
        tableRect.width -= scrollBarFrameRect.width + 3
        # pygame.draw.rect(window, Helpers.alterColorBrightness(frameColor, -30), tableRect)

        # ---> Scrollbar
        scrollBarRect = copy.deepcopy(navigationTopRect)
        scrollBarRect.height = scrollBarHeight

        if cls.__tableInfo[id]['scrollBarY'] is None:
            scrollBarRect.topleft = (navigationTopRect.left, navigationTopRect.bottom+3)
            cls.__tableInfo[id]['scrollBarY'] = navigationTopRect.bottom+3

        else:
            scrollBarRect.topleft = (navigationTopRect.left, cls.__tableInfo[id]['scrollBarY'])

        if cls.__mouseInfo['isLeftButtonPressed']:
            pointer = cls.__mouseInfo['pointer']

            scrollBarPosition = pointer[1]-scrollBarRect.height/2

            scrollBarClickableRect = pygame.Rect(
                scrollBarFrameRect.left,
                scrollBarFrameRect.top+navigationTopRect.height+3,
                scrollBarFrameRect.width,
                scrollBarFrameRect.height-navigationBottomRect.height-6-navigationTopRect.height-6
            )

            if scrollBarClickableRect.collidepoint(pointer):

                if scrollBarPosition > navigationTopRect.bottom and \
                        scrollBarPosition+scrollBarRect.height < navigationBottomRect.top:

                    cls.__tableInfo[id]['scrollBarY'] = pointer[1]-scrollBarRect.height/2
                    cls.__tableInfo[id]['dataPositionModifier'] = \
                        int(round(((cls.__tableInfo[id]['scrollBarY']-navigationTopRect.bottom+3)/scrollBarFrameScrollableAreaHeight)*totalDataHeight))

                elif scrollBarPosition < navigationTopRect.bottom:
                    cls.__tableInfo[id]['scrollBarY'] = navigationTopRect.bottom+3
                    cls.__tableInfo[id]['dataPositionModifier'] = 0

                elif scrollBarPosition+scrollBarRect.height > navigationBottomRect.top:
                    cls.__tableInfo[id]['scrollBarY'] = navigationBottomRect.top - scrollBarRect.height - 3
                    cls.__tableInfo[id]['dataPositionModifier'] = \
                        int(round(((cls.__tableInfo[id][
                                        'scrollBarY'] - navigationTopRect.bottom + 3) / scrollBarFrameScrollableAreaHeight) * totalDataHeight))

        scrollBarRect.topleft = (scrollBarRect.left, cls.__tableInfo[id]['scrollBarY'])
        pygame.draw.rect(window, cl.alterColorBrightness(frameColor, 40), scrollBarRect)

        # ---> Headers
        font = pygame.font.Font(None, 20)
        columnsWidth = []
        columnsLeft = []

        for x in range(noOfColumns):

            columnsLeft.append(innerFrameRect.left + sum(columnsWidth))
            columnsWidth.append(tableRect.width * columnWeight[x] / sum(columnWeight))

            # ---> Header box
            headerRect = pygame.Rect(0, 0, 0, 0)
            headerRect.width = (columnsWidth[x] - 2) if x<noOfColumns-1 else columnsWidth[x]
            headerRect.height = headerHeight
            headerRect.topleft = (columnsLeft[x], innerFrameRect.top)
            pygame.draw.rect(window, headerColor, headerRect)

            # ---> Header title
            text = font.render(data[0][x], 1, (255, 255, 255))
            textRect = text.get_rect()
            textRect.topleft = (headerRect.left+headerRect.width/2-textRect.width/2,
                                headerRect.top+headerRect.height/2-textRect.height/2)
            window.blit(text, textRect)

        # ---> Display data
        dataFrameRect = pygame.Rect(tableRect.left, tableRect.top+headerRect.height+headerMarginBottom, tableRect.width,
                                    tableRect.height-headerRect.height-headerMarginBottom)

        for x in range(1, len(data)):

            for y in range(noOfColumns):

                text = font.render(str(data[x][y]), 1, (255, 255, 255))
                textRect = text.get_rect()
                textRect.topleft = (columnsLeft[y]+3, innerFrameRect.top+(dataLineHeight*(x-1)+headerRect.height+5))
                textRect.top -= cls.__tableInfo[id]['dataPositionModifier']
                if dataFrameRect.contains(textRect):
                    window.blit(text, textRect)
                else:
                    break

    @classmethod
    def processEvents(cls, event):

        if event.type == MOUSEMOTION:
            cls.__mouseInfo['pointer'] = event.pos

        elif event.type == MOUSEBUTTONDOWN:
            cls.__mouseInfo['isLeftButtonPressed'] = True

        elif event.type == MOUSEBUTTONUP:
            cls.__mouseInfo['isLeftButtonPressed'] = False