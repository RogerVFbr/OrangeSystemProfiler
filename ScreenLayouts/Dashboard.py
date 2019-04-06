from DataGetters.DataGetters import DataGetters as dg
from Helpers.Helpers import Helpers as hp
from Resources.Colors import Colors as cl
from UIComponents.ExpandableList import ExpandableList
from UIComponents.HorizontalBar import HorizontalBar
from UIComponents.TitleBar import TitleBar


class Dashboard:

    @classmethod
    def draw(cls, window):

        TitleBar.draw(
            window = window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Dashboard'
        )

        listExtension = 384
        listLine1 = 128
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
            title='CPU',
            data={
                'BRAND': dg.getProcessorBrand()
                    if dg.getProcessorBrand() != '' else 'Unknown',
                'ARCHITECTURE': dg.getProcessorArchitecture()
                    if dg.getProcessorArchitecture() != '' else 'Unknown',
                'WORDLENGTH': (str(dg.getProcessorWordLength()) + ' bits')
                    if dg.getProcessorWordLength() != '' else 'Unknown',
                'FREQUENCY': (str(dg.getCpuFreq().current) + ' Hz') if dg.getCpuFreq() != '' else 'Unknown',
                'CORES': str(dg.getCores()) + ' (' + str(dg.getPhysicalCores()) + ' physical)',
            }
        )

        ExpandableList.draw(
            window = window,
            positionAndSize=(listLine1, listColumn2, listCaptionWidth, listCaptionHeight),
            dataBGExtension=listExtension,
            captionBGColor=cl.GOODSAMARITANBLUE,
            valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Memory',
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

        ExpandableList.draw(
            window = window,
            positionAndSize=(listLine2, listColumn1, listCaptionWidth, listCaptionHeight),
            dataBGExtension=listExtension,
            captionBGColor=cl.GOODSAMARITANBLUE,
            valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Disks',
            data={
                'TOTAL': (str(hp.convertBytesToGigabytes(dg.getDiskUsage().total)) + ' GB')
                    if dg.getDiskUsage() != '' else 'Unknown',
                'USED': (str(hp.convertBytesToGigabytes(dg.getDiskUsage().used)) + ' GB')
                    if dg.getDiskUsage() != '' else 'Unknown',
                'FREE': (str(hp.convertBytesToGigabytes(dg.getDiskUsage().free)) + ' GB')
                    if dg.getDiskUsage() != '' else 'Unknown',
                ' - ': '',
                '  -  ': '',
            }
        )

        ExpandableList.draw(
            window = window,
            positionAndSize=(listLine2, listColumn2, listCaptionWidth, listCaptionHeight),
            dataBGExtension=listExtension,
            captionBGColor=cl.GOODSAMARITANBLUE,
            valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Network',
            data={
                'HOST': dg.getDomainName() if dg.getDomainName() != '' else 'Unknown',
                'IP': dg.getIp() if dg.getIp() != '' else 'Unknown',
                'NETMASK': dg.getNetmask() if dg.getNetmask() != '' else 'Unknown',
                '-': '',
                ' - ': '',
            }
        )

        horizontalBarWidth = 250
        horizontalBarHeight = 30
        horizontalBarY = 558
        amountColor = cl.PURPLECORALLITE

        HorizontalBar.draw(
            window = window,
            caption='Memory Usage',
            unit='GB',
            totalValue=dg.getVirtualMemory().total if dg.getVirtualMemory() != '' else 100,
            currentValue=dg.getVirtualMemory().used if dg.getVirtualMemory() != '' else 0,
            positionAndSize=(10, horizontalBarY, horizontalBarWidth, horizontalBarHeight),
            barColor=cl.GRAY1,
            amountColor=amountColor
        )

        HorizontalBar.draw(
            window = window,
            caption='CPU Usage',
            unit='Hz',
            totalValue=dg.getCpuFreq().max if dg.getCpuFreq() != '' else 100,
            currentValue=(dg.getCpuPercentage() / 100 * dg.getCpuFreq().max) if dg.getCpuFreq() != '' else 0,
            positionAndSize=(274, horizontalBarY, horizontalBarWidth, horizontalBarHeight),
            barColor=cl.GRAY1,
            amountColor=amountColor
        )

        HorizontalBar.draw(
            window = window,
            caption='Disk Usage',
            unit='GB',
            totalValue=dg.getDiskUsage().total if dg.getDiskUsage() != '' else 1,
            currentValue=dg.getDiskUsage().used if dg.getDiskUsage() != '' else 0,
            positionAndSize=(538, horizontalBarY, horizontalBarWidth, horizontalBarHeight),
            barColor=cl.GRAY1,
            amountColor=amountColor
        )

