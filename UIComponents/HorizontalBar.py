import pygame

class HorizontalBar:

    @classmethod
    def draw(cls,
             window,
             caption = '',
             titleAlignment='center',
             unit = 'GB',
             totalValue = 0,
             currentValue = 0,
             positionAndSize = (0, 0, 0, 0),
             barColor = (50, 50, 50),
             amountColor = (200, 200, 200)):

        # ---> Draws total value bar
        pygame.draw.rect(window, barColor, positionAndSize)

        # ---> Draws total value caption
        dim = 80
        barCaptionColor = (
            barColor[0] - dim if barColor[0] > dim else 0,
            barColor[1] - dim if barColor[1] > dim else 0,
            barColor[2] - dim if barColor[2] > dim else 0)

        font = pygame.font.Font(None, 15)

        if unit is 'GB':
            barCaption = str(round(totalValue/(1024*1024*1024),1)) + ' GB'
        elif unit is 'Hz':
            barCaption = str(round(totalValue, 1)) + ' Hz'

        text = font.render(barCaption, 1, barCaptionColor)
        textRect = text.get_rect()
        textRect.topleft = (positionAndSize[0]+positionAndSize[2]-textRect.right-2, positionAndSize[1]+2)
        window.blit(text, textRect)

        # ---> Draws current value bar
        width = int(round((currentValue/totalValue)*positionAndSize[2]))
        # width = 130
        amountPositionAndSize = (positionAndSize[0]+1, positionAndSize[1]+1, ) + (width, ) + (positionAndSize[3]-2, )
        pygame.draw.rect(window, amountColor, amountPositionAndSize)

        # ---> Draws bar title
        font = pygame.font.Font(None, 25)
        text = font.render(caption, 1, (220, 220, 220))
        textRect = text.get_rect()
        textRect.topleft = (positionAndSize[0]+positionAndSize[2]/2-textRect.width/2, positionAndSize[1] - 25)
        window.blit(text, textRect)

        # ---> Draws bar current value percentage caption
        highlight = 70
        amountCaptionColor = (
            amountColor[0] + highlight if amountColor[0] <= 255 - highlight else 255,
            amountColor[1] + highlight if amountColor[1] <= 255 - highlight else 255,
            amountColor[2] + highlight if amountColor[2] <= 255 - highlight else 255)

        font = pygame.font.Font(None, 15)

        content = str(round((currentValue/totalValue)*100, 1)) + '%'
        text = font.render(content, 1, amountCaptionColor)
        textRect = text.get_rect()

        percentageTextPositionX = amountPositionAndSize[0] + amountPositionAndSize[2] - textRect.width - 3 if \
            amountPositionAndSize[0] + amountPositionAndSize[2] - textRect.width - 3 > amountPositionAndSize[0] +5 else \
                                    amountPositionAndSize[0]+5

        textRect.topleft = (percentageTextPositionX, amountPositionAndSize[1] + amountPositionAndSize[3] - 12)

        window.blit(text, textRect)

        # ---> Draws bar current value caption
        if unit is 'GB':
            content = str(round(currentValue/(1024*1024*1024),1)) + ' GB'
        elif unit is 'Hz':
            content = str(round(currentValue, 1)) + ' Hz'

        text = font.render(content, 1, amountCaptionColor)

        textRect = text.get_rect()

        currentValueTextPositionX = amountPositionAndSize[0] + amountPositionAndSize[2] - textRect.width - 3 if \
            amountPositionAndSize[0] + amountPositionAndSize[2] - textRect.width - 3 > amountPositionAndSize[0] +5 else \
                                    amountPositionAndSize[0]+5

        textRect.topleft = (currentValueTextPositionX, amountPositionAndSize[1] + amountPositionAndSize[3] - 25)
        window.blit(text, textRect.topleft)