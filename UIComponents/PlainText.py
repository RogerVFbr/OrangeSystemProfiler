import pygame

class PlainText:

    @classmethod
    def draw(self,
             window,
             fontSize = 15,
             fontColor = (250, 250, 250),
             position = (0, 0),
             content = 'Default'):

        font = pygame.font.Font(None, fontSize)
        text = font.render(content, 1, fontColor)
        textRect = text.get_rect()
        textRect.topleft = (position)
        window.blit(text, textRect)