from DataGetters.Logger import Logger as lg
from Resources.Colors import Colors as cl
from UIComponents.ScrollableTable import ScrollableTable
from UIComponents.TextInput import TextInput
from UIComponents.TitleBar import TitleBar


class Log:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window=window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Log'
        )

        TextInput.draw(
            id='log',
            window=window,
            caption='FILTER',
            positionAndSize=(10, 95, 780, 33),
            defaultInput='',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
        )

        ScrollableTable.draw(
            id='log',
            window=window,
            positionAndSize=(10, 140, 780, 450),
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
            data=lg.getLog(filter=TextInput.getTextInput('log')),
            columnWeight=[1.1, 1.7, 1.9, 7]
        )