import copy
import pygame
from Resources.Colors import Colors as cl
from pygame.locals import *


class TextInput:

    __txiContent = {}
    __mouseInfo = {
        'pointer': (0, 0),
        'isLeftButtonPressed': False,
        'isRightButtonPressed': False
    }

    @classmethod
    def draw(cls,
             id,
             window,
             positionAndSize=(10, 95, 780, 495),
             frameColor=(255, 255, 255),
             headerColor=(255, 255, 255),
             caption = '',
             defaultInput = '',
             padding=5,
             onEnterCallback = None):

        if id not in cls.__txiContent:
            cls.__txiContent[id] = { 'data': defaultInput,
                                     'isSelected': False,
                                     'rect': pygame.Rect(positionAndSize),
                                     'onEnterCallback': onEnterCallback }

        cls.__txiContent[id]['rect'] = pygame.Rect(positionAndSize)
        cls.__txiContent[id]['onEnterCallback'] = onEnterCallback

        pygame.draw.rect(window, frameColor, positionAndSize)

        # ---> Variables Definition
        textAreaMargin = 5
        captionHorizontalMargin = 15

        # ---> Inner Frame
        innerFrameRect = pygame.Rect(positionAndSize)
        innerFrameRect.topleft = (innerFrameRect.left + padding, innerFrameRect.top + padding)
        innerFrameRect.width -= padding * 2
        innerFrameRect.height -= padding * 2
        brightness = 10 if not cls.__txiContent[id]['isSelected'] else 60
        pygame.draw.rect(window, cl.alterColorBrightness(frameColor, brightness), innerFrameRect, 1)

        # ---> Caption Text
        fontSize = int(round((innerFrameRect.height-(2*textAreaMargin)) * 1.5))
        font = pygame.font.Font(None, fontSize)
        text = font.render(caption, 1, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (innerFrameRect.left+textAreaMargin+captionHorizontalMargin,
                            innerFrameRect.top+textAreaMargin)

        # ---> Caption Area
        captionAreaRect = pygame.Rect(0, 0, 0, 0)
        captionAreaRect.topleft = (innerFrameRect.left, innerFrameRect.top)
        captionAreaRect.width = textRect.width + textAreaMargin*2 + captionHorizontalMargin*2
        captionAreaRect.height = innerFrameRect.height
        brightness = cl.alterColorBrightness(frameColor, 20) if not cls.__txiContent[id]['isSelected'] else \
            cl.alterColorBrightness(frameColor, 50)
        pygame.draw.rect(window, brightness, captionAreaRect)
        window.blit(text, textRect)

        # ---> Text Area
        textAreaRect = pygame.Rect(innerFrameRect)
        textAreaRect.topleft = (innerFrameRect.left + textAreaMargin + captionAreaRect.width,
                                innerFrameRect.top + textAreaMargin)
        textAreaRect.width -= textAreaMargin * 2 + captionAreaRect.width
        textAreaRect.height -= textAreaMargin * 2
        # pygame.draw.rect(window, Helpers.alterColorBrightness(frameColor, 30), textAreaRect, 1)

        # ---> Data Display
        displayText = cls.__txiContent[id]['data']
        fontSize = int(round(textAreaRect.height * 1.5))
        font = pygame.font.Font(None, fontSize)
        text = font.render(displayText, 1, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (textAreaRect.left, textAreaRect.top)

        while textAreaRect.right<textRect.right:

            displayText = displayText[1:]
            text = font.render(displayText, 1, (255, 255, 255))
            rect = text.get_rect()
            textRect.width = rect.width

        window.blit(text, textRect)

    @classmethod
    def getTextInput(cls, id):
        if id in cls.__txiContent:
            return cls.__txiContent[id]['data']
        else:
            return ''

    @classmethod
    def processEvents(cls, event, ids):

        if event.type == MOUSEMOTION:
            cls.__mouseInfo['pointer'] = event.pos

        elif event.type == MOUSEBUTTONDOWN:
            cls.__mouseInfo['isLeftButtonPressed'] = True

            for x in cls.__txiContent:
                cls.__txiContent[x]['isSelected'] = False

            for x in ids:

                if x not in cls.__txiContent: continue

                if cls.__txiContent[x]['rect'].collidepoint(cls.__mouseInfo['pointer']):
                    cls.__txiContent[x]['isSelected'] = True
                    break




        elif event.type == MOUSEBUTTONUP:
            cls.__mouseInfo['isLeftButtonPressed'] = False

        elif event.type == KEYDOWN:

            for x in ids:

                if x not in cls.__txiContent: continue
                if not cls.__txiContent[x]['isSelected']: continue

                keysToIgnore = [
                    K_DELETE,
                    K_ESCAPE,
                    K_BACKSPACE,
                    K_RETURN
                ]

                if event.key not in keysToIgnore:
                    cls.__txiContent[x]['data'] += event.unicode

                elif event.key == K_DELETE or event.key == K_BACKSPACE:
                    cls.__txiContent[x]['data'] = cls.__txiContent[x]['data'][:-1]

                elif event.key == K_RETURN:
                    if cls.__txiContent[x]['onEnterCallback'] is not None:
                        cls.__txiContent[x]['onEnterCallback'][0](cls.__txiContent[x]['onEnterCallback'][1](cls.__txiContent[x]['onEnterCallback'][2]))


    @classmethod
    def getDataDisplayed(cls, data):
        pass





