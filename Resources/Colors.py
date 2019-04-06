class Colors:

    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (0xFF, 0xFF, 0xFF)
    PINK = (0xFF, 0x65, 0xFD)

    GRAY1 = (149, 165, 166)
    PURPLE = (122, 48, 153)
    MATTPURPLE = (140, 122, 230)

    MIDNIGHTBLUE = (44, 62, 80)
    BELIZEBLUE = (41, 128, 185)
    NAVALBLUE = (64, 115, 158)
    GOODSAMARITANBLUE = (60, 99, 130)

    MAZARINEBLUE = (39, 60, 117)
    AURORAGREEN = (120, 224, 143)
    JALAPENORED = (183, 21, 64)
    CARROTORANGE = (229, 142, 38)
    DEEPROSE = (196, 69, 105)
    PURPLECORALLITE = (87, 75, 144)


    @classmethod
    def alterColorBrightness(self, color, brightness):

        if brightness > 0:

            return (
                color[0] + brightness if color[0] <= 255 - brightness else 255,
                color[1] + brightness if color[1] <= 255 - brightness else 255,
                color[2] + brightness if color[2] <= 255 - brightness else 255
            )

        else:

            return (
                color[0] + brightness if color[0] > -brightness else 0,
                color[1] + brightness if color[1] > -brightness else 0,
                color[2] + brightness if color[2] > -brightness else 0
            )
