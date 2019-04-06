from DataGetters.DataGetters import DataGetters as dg
from Helpers.Helpers import Helpers as hp
from Resources.Colors import Colors as cl
from UIComponents.ExpandableList import ExpandableList
from UIComponents.TitleBar import TitleBar


class Disks:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window = window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Disks'
        )

        listExtension = 384
        listLine1 = 95
        listLine2 = 342
        listColumn1 = 10
        listColumn2 = 405
        listCaptionWidth = 110
        listCaptionHeight = 30

        ExpandableList.draw(
            window = window,
            positionAndSize=(listLine1, listColumn1, listCaptionWidth, listCaptionHeight),
            dataBGExtension=listExtension,
            captionBGColor=cl.GOODSAMARITANBLUE,
            valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='',
            data={
                'TOTAL': (str(hp.convertBytesToGigabytes(dg.getDiskUsage().total)) + ' GB')
                    if dg.getDiskUsage() != '' else 'Unknown',
                'USED': (str(hp.convertBytesToGigabytes(dg.getDiskUsage().used)) + ' GB')
                    if dg.getDiskUsage() != '' else 'Unknown',
                'FREE': (str(hp.convertBytesToGigabytes(dg.getDiskUsage().free)) + ' GB')
                    if dg.getDiskUsage() != '' else 'Unknown'
            }
        )