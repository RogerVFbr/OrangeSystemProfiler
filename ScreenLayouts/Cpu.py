from DataGetters.DataGetters import DataGetters as dg
from Resources.Colors import Colors as cl
from UIComponents.ExpandableList import ExpandableList
from UIComponents.MultiVerticalBars import MultiVerticalBars
from UIComponents.TitleBar import TitleBar


class Cpu:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window = window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='CPU'
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
                'BRAND': dg.getProcessorBrand()
                    if dg.getProcessorBrand() != '' else 'Unknown',
                'ARCHITECTURE': dg.getProcessorArchitecture()
                    if dg.getProcessorArchitecture() != '' else 'Unknown',
                'WORDLENGTH': (str(dg.getProcessorWordLength()) + ' bits')
                    if dg.getProcessorWordLength() != '' else 'Unknown',
                'FREQUENCY': (str(dg.getCpuFreq().current) + ' Hz')
                    if dg.getCpuFreq() != '' else 'Unknown',
                'CORES': str(dg.getCores()) + ' (' + str(dg.getPhysicalCores()) + ' physical)',
            }
        )

        ExpandableList.draw(
            window = window,
            positionAndSize=(listLine1, listColumn2, listCaptionWidth, listCaptionHeight),
            dataBGExtension=listExtension,
            captionBGColor=cl.GOODSAMARITANBLUE,
            valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='',
            data={
                'ACTUAL SPEED': dg.getProcessorActualSpeed() if dg.getProcessorActualSpeed() != '' else 'Unknown',
                'L2 SIZE': dg.getProcessorL2Size() if dg.getProcessorL2Size() != '' else 'Unknown',
                'L2 LINE': dg.getProcessorL2Line() if dg.getProcessorL2Line() != '' else 'Unknown',
                'L2 ASSOC.': dg.getProcessorL2Assoc() if dg.getProcessorL2Assoc() != '' else 'Unknown',
            }
        )

        windowWidth = window.get_rect().width
        marginHorizontal = 10

        averaging = 60

        if dg.isRemote():
            averaging = 20

        MultiVerticalBars.draw(
            id='cpucores',
            window = window,
            positionAndSize=(marginHorizontal, 278, windowWidth - marginHorizontal * 2, 310),
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            padding=5,
            percentageList=dg.getPerCoreUsage(),
            averaging=averaging
        )