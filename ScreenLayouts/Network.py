from DataGetters.TableFormatters import TableFormatters as tf
from Resources.Colors import Colors as cl
from UIComponents.ScrollableTable import ScrollableTable
from UIComponents.TitleBar import TitleBar


class Network:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window=window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Network'
        )

        ScrollableTable.draw(
            window = window,
            id='network',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
            positionAndSize=(10, 95, 780, 240),
            data=tf.getNetworkForTable(),
            columnWeight=[1, 3]
        )

        ScrollableTable.draw(
            window=window,
            id='processes_network',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
            positionAndSize=(10, 348, 780, 240),
            data=tf.getProcessesNetworkUsageForTable(),
            columnWeight=[0.2, 0.3, 0.4, 1, 1]
        )