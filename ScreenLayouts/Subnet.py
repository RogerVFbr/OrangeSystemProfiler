from DataGetters.DataGetters import DataGetters as dg
from DataGetters.TableFormatters import TableFormatters as tf
from Resources.Colors import Colors as cl
from UIComponents.ScrollableTable import ScrollableTable
from UIComponents.TextInput import TextInput
from UIComponents.TitleBar import TitleBar


class Subnet:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window = window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Subnet'
        )

        TextInput.draw(
            id='subnet',
            window=window,
            caption='SUBNET',
            positionAndSize=(10, 95, 780, 33),
            defaultInput='',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            onEnterCallback=(dg.updateHosts, TextInput.getTextInput, 'subnet'),
            headerColor=cl.GOODSAMARITANBLUE,
        )

        ScrollableTable.draw(
            id='subnet',
            window=window,
            positionAndSize=(10, 140, 780, 450),
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
            data=tf.getSubnetForTable(),
            columnWeight=[1, 3]
        )

