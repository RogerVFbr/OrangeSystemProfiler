from DataGetters.DataGetters import DataGetters as dg
from Helpers.Helpers import Helpers as hp
from Resources.Colors import Colors as cl
from UIComponents.ExpandableList import ExpandableList
from UIComponents.TitleBar import TitleBar


class Memory:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window = window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Memory'
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
                'TOTAL': (str(hp.convertBytesToGigabytes(dg.getVirtualMemory().total)) + ' GB')
                    if dg.getVirtualMemory() != '' else 'Unknown',
                'AVAILABLE': (str(hp.convertBytesToGigabytes(dg.getVirtualMemory().available)) + ' GB')
                    if dg.getVirtualMemory() != '' else 'Unknown',
                'PERCENT': (str(dg.getVirtualMemory().percent) + ' %')
                    if dg.getVirtualMemory() != '' else 'Unknown',
                'USED': (str(hp.convertBytesToGigabytes(dg.getVirtualMemory().used)) + ' GB')
                    if dg.getVirtualMemory() != '' else 'Unknown',
                'FREE': (str(hp.convertBytesToGigabytes(dg.getVirtualMemory().free)) + ' GB')
                    if dg.getVirtualMemory() != '' else 'Unknown',
            }
        )