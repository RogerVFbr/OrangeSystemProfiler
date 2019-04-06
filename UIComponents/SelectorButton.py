import pygame
from Resources.Colors import Colors as cl
from pygame.locals import *


class SelectorButton:

    __props = dict()
    __positionAndSize = dict()
    __mouseInfo = {
        'pointer': (0, 0),
        'isLeftButtonPressed': False,
        'isRightButtonPressed': False
    }

    @classmethod
    def draw(cls,
             id,
             window,
             positionAndSize=(20, 20, 20, 20),
             fontColor = (250, 250, 250),
             selectedBGColor=(100, 100, 100),
             unselectedBGColor  = (200, 200, 200),
             selectedCaption = 'BUTTON',
             unselectedCaption = 'BUTTON',
             fontSize = 15,
             initialState = False,
             deactivatable = True,
             onActivate = None,
             onDeactivate = None,
             onChange = None
             ):

        if id not in cls.__props:
            cls.__props[id] = {
                'isSelected' : initialState,
                'positionAndSize': positionAndSize,
                'deactivatable': deactivatable,
                'onActivate': onActivate,
                'onDeactivate': onDeactivate,
                'onChange': onChange}

        cls.__props[id]['onActivate'] = onActivate
        cls.__props[id]['onDeactivate'] = onDeactivate
        cls.__props[id]['onChange'] = onChange

        windowRect = window.get_rect()
        position = pygame.Rect(positionAndSize)
        button_bgcolor = selectedBGColor if cls.__props[id]['isSelected'] else unselectedBGColor
        pygame.draw.rect(window, button_bgcolor, position)

        font = pygame.font.Font(None, fontSize)
        text = font.render(selectedCaption if cls.__props[id]['isSelected'] else unselectedCaption, 1, fontColor)
        textRect = text.get_rect()
        textRect.topleft = (position.left+position.width/2-textRect.width/2,
                            position.top+position.height/2-textRect.height/2)
        window.blit(text, textRect)

    @classmethod
    def processEvents(cls, event, ids):

        if event.type == MOUSEMOTION:
            cls.__mouseInfo['pointer'] = event.pos

        elif event.type == MOUSEBUTTONDOWN:
            cls.__mouseInfo['isLeftButtonPressed'] = True

            for x in ids:

                if x not in cls.__props: continue

                if pygame.Rect(cls.__props[x]['positionAndSize']).collidepoint(cls.__mouseInfo['pointer']):

                    if not cls.__props[x]['deactivatable'] and cls.__props[x]['isSelected']: return

                    cls.__props[x]['isSelected'] = not cls.__props[x]['isSelected']

                    if type(cls.__props[x]['onChange']) == tuple or type(cls.__props[x]['onChange']) == list:

                        for y in cls.__props[x]['onChange']:
                            if type(y) != tuple:
                                y()
                            else:
                                y[0](y[1])

                    if cls.__props[x]['isSelected'] and (type(cls.__props[x]['onActivate']) == tuple or
                                                         type(cls.__props[x]['onActivate']) == list):

                        for y in cls.__props[x]['onActivate']:
                            if type(y) != tuple:
                                y()
                            else:
                                y[0](y[1])

                    if not cls.__props[x]['isSelected'] and (type(cls.__props[x]['onDeactivate']) == tuple or
                                                         type(cls.__props[x]['onDeactivate']) == list):

                        for y in cls.__props[x]['onDeactivate']:
                            if type(y) != tuple:
                                y()
                            else:
                                y[0](y[1])


        elif event.type == MOUSEBUTTONUP:

            cls.__mouseInfo['isLeftButtonPressed'] = False

    @classmethod
    def activate(cls, id):
        if id in cls.__props:
            cls.__props[id]['isSelected'] = True
            # if (type(cls.__props[id]['onActivate']) == tuple or type(cls.__props[id]['onActivate']) == list):
            #     for y in cls.__props[id]['onActivate']:
            #         if type(y) != tuple:
            #             y()
            #         else:
            #             y[0](y[1])



    @classmethod
    def deactivate(cls, id):
        if id in cls.__props:
            cls.__props[id]['isSelected'] = False
            # if type(cls.__props[id]['onDeactivate']) == tuple:
            #     for y in cls.__props[id]['onDeactivate']:
            #         if type(y) != tuple:
            #             y()
            #         else:
            #             y[0](y[1])

    @classmethod
    def toggle(cls, id):
        if id in cls.__props:
            cls.__props[id]['isSelected'] = not cls.__props[id]['isSelected']

    @classmethod
    def isSelected(cls, id):
        if id in cls.__props:
            return cls.__props[id]['isSelected']
        return False



