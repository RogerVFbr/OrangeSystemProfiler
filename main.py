# from pygame.locals import *
# import pygame

from DataGetters.SubnetFinder import SubnetFinder
from Resources.Colors import Colors as cl

from ScreenLayouts.Cpu import Cpu
from ScreenLayouts.Dashboard import Dashboard
from ScreenLayouts.FileBrowser import FileBrowser
from ScreenLayouts.Log import Log
from ScreenLayouts.Memory import Memory
from ScreenLayouts.Network import Network
from ScreenLayouts.Processes import Processes
from ScreenLayouts.Disks import Disks
from ScreenLayouts.Sharing import Sharing
from ScreenLayouts.Subnet import Subnet

from UIComponents.ScrollableTable import ScrollableTable
from UIComponents.SelectorButton import SelectorButton
from UIComponents.TextInput import TextInput
from UIComponents.TopMenu import TopMenu


if __name__ == '__main__':

    from pygame.locals import *
    import pygame

    pygame.init()
    SCREENWIDTH = 800
    SCREENHEIGHT = 600
    WINDOW = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Orange System Profiler")
    pygame.display.init()
    clock = pygame.time.Clock()
    running = True

    # ---> Main Loop
    while running:

        # ---> Events Processing
        for event in pygame.event.get():

            if event.type == pygame.QUIT: running = False

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE: running = False

                elif event.key == K_SPACE:
                    if not TopMenu.isSelected('File Browser') and \
                            not TopMenu.isSelected('Log') and \
                            not TopMenu.isSelected('Subnet'):
                        TopMenu.setSelectionAsHome()

            TopMenu.processEvents(event)
            ScrollableTable.processEvents(event)
            if TopMenu.isSelected('Sharing'):
                SelectorButton.processEvents(event, ['local', 'remote', 'broadcast'])
                TextInput.processEvents(event, ['broadcast_port', 'remote_host', 'remote_port'])
            if TopMenu.isSelected('File Browser'): TextInput.processEvents(event, ['filebrowser'])
            if TopMenu.isSelected('Subnet'): TextInput.processEvents(event, ['subnet'])
            if TopMenu.isSelected('Log'): TextInput.processEvents(event, ['log'])

        # ---> Draw graphics
        WINDOW.fill(cl.MIDNIGHTBLUE)

        TopMenu.draw(
            window=WINDOW,
            menuItems=['Dashboard', 'CPU', 'Memory', 'Disks', 'Processes',
                       'File Browser', 'Network', 'Subnet', 'Sharing', 'Log']
        )

        if TopMenu.isSelected('Dashboard'):       Dashboard.draw(WINDOW)
        elif TopMenu.isSelected('CPU'):           Cpu.draw(WINDOW)
        elif TopMenu.isSelected('Memory'):        Memory.draw(WINDOW)
        elif TopMenu.isSelected('Disks'):         Disks.draw(WINDOW)
        elif TopMenu.isSelected('Network'):       Network.draw(WINDOW)
        elif TopMenu.isSelected('Processes'):     Processes.draw(WINDOW)
        elif TopMenu.isSelected('File Browser'):  FileBrowser.draw(WINDOW)
        elif TopMenu.isSelected('Subnet'):        Subnet.draw(WINDOW)
        elif TopMenu.isSelected('Sharing'):       Sharing.draw(WINDOW)
        elif TopMenu.isSelected('Log'):           Log.draw(WINDOW)

        # ---> Update display and tick
        pygame.display.update()
        clock.tick(60)

    pygame.display.quit()



