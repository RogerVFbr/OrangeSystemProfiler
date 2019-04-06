import pygame
from pygame.locals import *

from Helpers.Helpers import Helpers
from Resources.Colors import Colors as cl


class TopMenu:

    __TAG = 'TopMenu: '
    __menuItems = []

    __mouseInfo = {
        'pointer': (0, 0),
        'isLeftButtonPressed': False,
        'isRightButtonPressed': False
    }

    @classmethod
    def draw(cls,
             window,
             height=30,
             menuItems=[],
             fontColor=(0, 0, 0),
             bgColor=(200, 200, 200),
             highlightBrightness=-20
             ):

        
        pointer = cls.__mouseInfo['pointer']

        itemSpacing = 15

        position = pygame.Rect(0, 0, window.get_width(), height)
        pygame.draw.rect(window, bgColor, position)

        logo = pygame.image.load('Resources/images/Orange.png')
        logoMargin = (10, 5)
        window.blit(logo, logoMargin)

        logoOffset = logo.get_rect().width + logoMargin[0] + itemSpacing

        itemOffset = logoOffset

        for x in range(len(menuItems)):
            font = pygame.font.Font(None, 20)
            text = font.render(menuItems[x], 1, fontColor)
            textRect = text.get_rect()
            textRect.topleft = (itemOffset, 9)

            itemHighlightZone = pygame.Rect(itemOffset - int(round(itemSpacing / 2)),
                                            0,
                                            textRect.width + itemSpacing,
                                            height)

            if itemHighlightZone.collidepoint(pointer):
                itemHighlightRect = pygame.Rect(
                    itemOffset - int(round(itemSpacing / 2)),
                    3,
                    textRect.width + itemSpacing,
                    height - 5)
                pygame.draw.rect(window, cl.alterColorBrightness(bgColor, highlightBrightness), itemHighlightRect)

            window.blit(text, textRect)

            if len(cls.__menuItems) < len(menuItems):
                menuItemData = [menuItems[x], itemHighlightZone, False]
                cls.__menuItems.append(menuItemData)
                cls.__menuItems[0][2] = True

            itemOffset += textRect.width + itemSpacing

    @classmethod
    def setSelection(cls, selection):

        indexSelected = None

        if type(selection) is tuple and len(selection) is 2:

            for x in range(len(cls.__menuItems)):
                if cls.__menuItems[x][1].collidepoint(selection):
                    indexSelected = x
                    break

        elif type(selection) is str:

            for x in range(len(cls.__menuItems)):
                if cls.__menuItems[x][0] is selection:
                    indexSelected = x
                    break

        elif type(selection) is int:

            indexSelected = selection

        if indexSelected is not None:

            for x in range(len(cls.__menuItems)):
                cls.__menuItems[x][2] = False
            cls.__menuItems[indexSelected][2] = True

    @classmethod
    def setSelectionToNext(cls):

        index = [i for i, elem in enumerate(cls.__menuItems) if cls.__menuItems[i][2] is True][0]
        cls.__menuItems[index][2] = False

        index += 1
        if index >= len(cls.__menuItems):
            index = 0
        cls.__menuItems[index][2] = True

    @classmethod
    def setSelectionToPrevious(cls):

        index = [i for i, elem in enumerate(cls.__menuItems) if cls.__menuItems[i][2] is True][0]
        cls.__menuItems[index][2] = False

        index -= 1
        if index < 0:
            index = len(cls.__menuItems)-1
        cls.__menuItems[index][2] = True

    @classmethod
    def setSelectionAsHome(cls):
        cls.setSelection(0)

    @classmethod
    def isSelected(cls, item):
        for x in cls.__menuItems:
            if x[0] is item:
                if x[2]: return True
                else: return False
        return False

    @classmethod
    def processEvents(cls, event):

        if event.type == KEYDOWN:

            if event.key == K_LEFT:
                cls.setSelectionToPrevious()

            elif event.key == K_RIGHT:
                cls.setSelectionToNext()

        elif event.type == MOUSEMOTION:
            TopMenu.__mouseInfo['pointer'] = event.pos

        elif event.type == MOUSEBUTTONDOWN:
            cls.__mouseInfo['isLeftButtonPressed'] = True
            cls.setSelection(cls.__mouseInfo['pointer'])

        elif event.type == MOUSEBUTTONUP:
            cls.__mouseInfo['isLeftButtonPressed'] = False
