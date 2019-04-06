import pygame

class TitleBar:

    @classmethod
    def draw(self,
             window,
             height = 40,
             marginTop = 42,
             marginSides = 10,
             fontSize = 30,
             fontColor = (250, 250, 250),
             bgColor  = (200, 200, 200),
             title = 'TEST'):

        windowRect = window.get_rect()
        position = pygame.Rect(marginSides, marginTop, windowRect.width-marginSides*2, height)
        pygame.draw.rect(window, bgColor, position)

        font = pygame.font.Font(None, fontSize)
        text = font.render(title, 1, fontColor)
        textRect = text.get_rect()
        textRect.topleft = (marginSides+position.width/2-textRect.width/2,
                            marginTop+position.height/2-textRect.height/2+3)
        window.blit(text, textRect)