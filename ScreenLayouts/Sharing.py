from DataGetters.DataGetters import DataGetters as dg
from DataGetters.RemoteData import RemoteData as rd
from DataGetters.Broadcaster import Broadcaster as bc
from Resources.Colors import Colors as cl
from UIComponents.ExpandableList import ExpandableList
from UIComponents.ScrollableTable import ScrollableTable
from UIComponents.SelectorButton import SelectorButton
from UIComponents.TextInput import TextInput
from UIComponents.TitleBar import TitleBar


class Sharing:

    @classmethod
    def draw(cls, window):

        v0ff = 30

        TitleBar.draw(
            window = window,
            bgColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='Sharing'
        )

        SelectorButton.draw(
            id = 'local',
            window = window,
            selectedCaption = 'LOCAL DATA',
            unselectedCaption = 'LOCAL DATA',
            fontSize=25,
            selectedBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 20),
            unselectedBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 5),
            positionAndSize=(10, 100+v0ff, 780, 80),
            initialState=True,
            deactivatable=False,
            onActivate = ((SelectorButton.deactivate, 'remote'), dg.setLocalData),
        )

        host = TextInput.getTextInput('remote_host')
        port = TextInput.getTextInput('remote_port')


        SelectorButton.draw(
            id='remote',
            window=window,
            selectedCaption='REMOTE DATA',
            unselectedCaption='REMOTE DATA',
            fontSize=25,
            selectedBGColor = cl.alterColorBrightness(cl.MIDNIGHTBLUE, 20),
            unselectedBGColor = cl.alterColorBrightness(cl.MIDNIGHTBLUE, 5),
            deactivatable=False,
            positionAndSize=(10, 200+v0ff, 780, 80),
            onActivate= ((SelectorButton.deactivate, 'local'), (dg.setRemoteData, [host, port])),
        )

        TextInput.draw(
            id='remote_host',
            window=window,
            caption='HOST',
            positionAndSize=(10, 285+v0ff, 387, 33),
            defaultInput='',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
        )

        TextInput.draw(
            id='remote_port',
            window=window,
            caption='PORT',
            positionAndSize=(403, 285+v0ff, 387, 33),
            defaultInput='',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
        )

        ExpandableList.draw(
            window=window,
            positionAndSize=(323+v0ff, 10, 82, 30),
            dataBGExtension=780,
            captionBGColor=cl.GOODSAMARITANBLUE,
            valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='',
            data={
                'STATUS': rd.getMessage(),
            }
        )

        SelectorButton.draw(
            id='broadcast',
            window=window,
            unselectedCaption='BROADCAST',
            selectedCaption='BROADCASTING ...',
            fontSize=25,
            selectedBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 20),
            unselectedBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 5),
            positionAndSize=(10, 375+v0ff, 780, 80),
            onActivate=((bc.startBroadcasting, TextInput.getTextInput('broadcast_port')),),
            onDeactivate=(bc.stopBroadcasting,)
        )

        TextInput.draw(
            id='broadcast_port',
            window=window,
            caption='PORT',
            positionAndSize=(10, 460+v0ff, 780, 33),
            defaultInput='',
            frameColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            headerColor=cl.GOODSAMARITANBLUE,
        )

        ExpandableList.draw(
            window=window,
            positionAndSize=(498+v0ff, 10, 82, 30),
            dataBGExtension=780,
            captionBGColor=cl.GOODSAMARITANBLUE,
            valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
            title='',
            data={
                'STATUS': bc.getMessage(),
            }
        )

        if SelectorButton.isSelected('broadcast'):

            ExpandableList.draw(
                window=window,
                positionAndSize=(388+v0ff, 580, 45, 25),
                fontSize=17,
                dataBGExtension=200,
                captionBGColor=cl.GOODSAMARITANBLUE,
                valueBGColor=cl.alterColorBrightness(cl.MIDNIGHTBLUE, 10),
                title='',
                data={
                    'IP': bc.getBroadcastAddress()[2],
                    'PORT': bc.getBroadcastAddress()[1]
                }
            )


