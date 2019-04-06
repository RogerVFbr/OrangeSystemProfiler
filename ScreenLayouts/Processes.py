from DataGetters.TableFormatters import TableFormatters as tf
from Resources.Colors import Colors as cl
from UIComponents.ScrollableTable import ScrollableTable
from UIComponents.TitleBar import TitleBar


class Processes:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window=window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Processes'
        )

        ScrollableTable.draw(
            window = window,
            id='processes',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
            data=tf.getProcessesForTable(),
            columnWeight=[1, 3, 1, 1, 3, 1]
        )