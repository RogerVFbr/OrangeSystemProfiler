from DataGetters.DataGetters import DataGetters as dg
from DataGetters.TableFormatters import TableFormatters as tf
from Resources.Colors import Colors as cl
from UIComponents.PlainText import PlainText
from UIComponents.ScrollableTable import ScrollableTable
from UIComponents.TextInput import TextInput
from UIComponents.TitleBar import TitleBar


class FileBrowser:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window=window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='File Browser'
        )

        if dg.isLocal():

            TextInput.draw(
                id='filebrowser',
                window=window,
                caption='PATH',
                positionAndSize=(10, 95, 780, 33),
                defaultInput=dg.getCurrentWorkingDirectory(),
                frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
                headerColor=cl.GOODSAMARITANBLUE,
            )

            ScrollableTable.draw(
                id='filebrowser',
                window=window,
                positionAndSize=(10, 140, 780, 450),
                frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
                headerColor=cl.GOODSAMARITANBLUE,
                data=tf.getFilesAndFoldersForTable(TextInput.getTextInput('filebrowser')),
                columnWeight=[3, 1, 0.65, 1.4, 1.4]
            )

        else:

            PlainText.draw(
                window = window,
                position = (10, 95),
                fontSize=20,
                content='Current: ' + dg.getCurrentWorkingDirectory()
            )

            TextInput.draw(
                id='filebrowser',
                window=window,
                caption='PATH',
                positionAndSize=(10, 120, 780, 33),
                defaultInput=dg.getCurrentWorkingDirectory(),
                frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
                headerColor=cl.GOODSAMARITANBLUE,
            )

            ScrollableTable.draw(
                id='filebrowser',
                window=window,
                positionAndSize=(10, 165, 780, 425),
                frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
                headerColor=cl.GOODSAMARITANBLUE,
                data=tf.getFilesAndFoldersForTable(TextInput.getTextInput('filebrowser')),
                columnWeight=[3, 1, 0.65, 1.4, 1.4]
            )
