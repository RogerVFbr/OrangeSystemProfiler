import datetime
import time
import collections
from Helpers.Helpers import Helpers as hl
from DataGetters.DataGetters import DataGetters as dg


class TableFormatters:

    __TAG = 'TableFormatters: '

    @classmethod
    def getProcessesForTable(cls):

        processesList = dg.getProcesses()
        processesForTable = []
        processesForTable.append(['PID', 'NAME', 'CPU%', 'MEM%', 'USERNAME', 'THREADS'])

        if processesList == '':
            processesForTable.append(['Awaiting server...', '', '', '', '', ''])
            return processesForTable

        for k in range(len(processesList)):
            processData = []
            processData.append(processesList[k]['pid'])
            processData.append(processesList[k]['name'])
            processData.append(processesList[k]['cpu_percent'])
            if 'memory_percent' not in processesList[k]:
                processData.append('-')
            else:
                try:
                    processData.append(str(round(processesList[k]['memory_percent'], 2)) + '%')
                except Exception as error:
                    # print(error)
                    processData.append('Unknown')
            processData.append(processesList[k]['username'] if processesList[k]['username'] is not None else '-')
            if processesList[k]['num_threads'] == None:
                processData.append('-')
            else:
                processData.append(processesList[k]['num_threads'])

            processesForTable.append(processData)

        return processesForTable

    @classmethod
    def getNetworkForTable(cls):

        networksForTable = []
        networksForTable.append(['NIC', 'DETAILS'])

        data = dg.getNetworkInfo()

        if data == '':
            networksForTable.append(['Awaiting server...', ''])
            return networksForTable

        networksList, dataTraffic, ioCounters = dg.getNetworkInfo()

        for x in networksList:

            networksForTable.append([x, '{}, {} (Speed: {}, MTU: {})'.format(
                hl.decodeNICactivity(dataTraffic[x].isup),
                hl.decodeNICcomType(dataTraffic[x].duplex),
                dataTraffic[x].speed,
                dataTraffic[x].mtu
            )])

            networksForTable.append(['', ''])

            if x in ioCounters:
                networksForTable.append(['   Bytes (Sent/Recv)', str(ioCounters[x].bytes_sent) + ' / ' + str(ioCounters[x].bytes_recv)])
                networksForTable.append(['   Packets (Sent/Recv)', str(ioCounters[x].packets_sent) + ' / ' + str(ioCounters[x].packets_recv)])
                networksForTable.append(['   Errors (I/O)', str(ioCounters[x].errin) + ' / ' + str(ioCounters[x].errout)])
                networksForTable.append(['   Dropped (I/O)', str(ioCounters[x].dropin) + ' / ' + str(ioCounters[x].dropout)])

            else:
                networksForTable.append(['   Bytes (Sent/Recv)', 'Unknown'])
                networksForTable.append(['   Packets (Sent/Recv)', 'Unknown'])
                networksForTable.append(['   Errors (I/O)', 'Unknown'])
                networksForTable.append(['   Dropped (I/O)', 'Unknown'])

            networksForTable.append(['', ''])

            for i in networksList[x]:
                data = str(i.address)
                if i.netmask != None:
                    data += ' | Netmask: ' + i.netmask
                if i.broadcast != None:
                    data += ' | Broadcast: ' + i.broadcast
                if i.ptp != None:
                    data += ' | PTP: ' + i.ptp

                networksForTable.append(['   ' + hl.convertFamilyToAddType(i.family), data])

            networksForTable.append(['', ''])

        return networksForTable

    @classmethod
    def getProcessesNetworkUsageForTable(cls):

        p = dg.getProcessesNetworkUsage()
        processesForTable = []
        processesForTable.append(['PID', 'TYPE', 'STATUS', 'LOCAL', 'REMOTE'])

        if isinstance(p, str) and p == '':
            processesForTable.append(['Awaiting server...', '', '', '', ''])
            return processesForTable;

        if len(p) == 0 or len(p) == 1:
            processesForTable.append(['Fetching data...', '', '', '', ''])
            return processesForTable;

        for k, v in p.items():

            if not isinstance(k, int): continue
            if len(v) == 0: continue

            for x in range(len(v)):

                try:

                    newLine = [
                        k,
                        hl.convertFamilyToAddType(v[x].family) + " | " + hl.convertToSocketType(v[x].type),
                        v[x].status,
                        (v[x].laddr[0] + ' (' + str(v[x].laddr[1]) + ')') if len(v[x].laddr)>0 else '',
                        (v[x].raddr[0] + ' (' + str(v[x].raddr[1]) + ')') if len(v[x].raddr)>0 else '',
                    ]

                except Exception as error:
                    continue

                if x>0: newLine[0] = ''
                processesForTable.append(newLine)

        return processesForTable

    @classmethod
    def getFilesAndFoldersForTable(cls, path):

        dataForTable = []
        dataForTable.append(['NAME', 'SIZE', 'TYPE', 'ACCESSED', 'MODIFIED'])

        data = dg.getFilesAndFoldersOnPath(path)

        if data == '':
            dataForTable.append(['Awaiting server response...', '', '', '', ''])
            return dataForTable

        foldersList, filesList = dg.getFilesAndFoldersOnPath(path)

        if len(foldersList) is 0 and len(filesList) is 0:
            dataForTable.append(['Invalid or empty path.', '', '', '', ''])
            return dataForTable

        for k in range(len(foldersList)):
            processData = []
            processData.append(foldersList[k]['name'])
            processData.append('')
            processData.append('Folder')
            processData.append('')
            processData.append('')

            dataForTable.append(processData)

        for k in range(len(filesList)):
            processData = []
            processData.append(hl.limitFileNameLength(filesList[k]['name'], 40))
            processData.append(str(hl.convertBytesToKilobytes(filesList[k]['size'])) + " Kb")
            processData.append('File')
            processData.append(datetime.datetime.fromtimestamp(filesList[k]['accessed']).strftime('%d.%m.%Y %H:%M:%S'))
            processData.append(datetime.datetime.fromtimestamp(filesList[k]['modified']).strftime('%d.%m.%Y %H:%M:%S'))

            dataForTable.append(processData)

        return dataForTable

    @classmethod
    def getSubnetForTable(cls):

        hosts = dg.getHosts()
        returnData = []
        returnData.append(['PROPERTY', 'VALUE'])

        if isinstance(hosts, str):
            returnData.append(['Awaiting server response...', ''])
            return returnData

        if hosts['status'] == 'fetching':
            returnData.append(['Mapping ...'.format(hosts['ip']), hosts['details'] +
                               ' (Elapsed: ' +
                               hl.convertSecsToHHMMSS(time.time() - hosts['starttime']) + ')'])

        elif hosts['status'] == 'invalid':
            returnData.append(['Invalid input.', ''])

        elif hosts['status'] == 'fetching_details' or hosts['status'] == 'ready':

            if hosts['status'] == 'fetching_details':

                returnData.append(["Fetching details ...", hosts['details'] +
                                   ' (Elapsed: ' +
                                   hl.convertSecsToHHMMSS(time.time() - hosts['starttime']) + ')'])
                returnData.append(['', ''])

            elif hosts['status'] == 'ready':

                returnData.append([
                    "Mapping on {} ready.".format(hosts['ip']),
                    'Finished in {} | {} IPs analyzed | Avg. scan time: {} | {} worker threads.'
                        .format(hl.convertSecsToHHMMSS(hosts['finishtime'] - hosts['starttime']),
                                len(hosts['valid_hosts']),
                                hl.convertSecsToHHMMSS(hosts['avg_scan_time']),
                                hosts['no_of_workers']
                                )])
                returnData.append(['', ''])

            for key, value in dict(hosts['host_details']).items():

                returnData.append(['Hosts at ' + str(key), 'Scan time: ' +
                                   hl.convertSecsToHHMMSS(value['elapsed'])])

                for y in value['hostnames']:
                    if y['name'] != '':
                        returnData.append(['    Name:', y['name']])
                    if y['type'] != '':
                        returnData.append(['    Type:', y['type']])

                for y, z in value['addresses'].items():
                    returnData.append(['    ' + str(y), str(z)])

                returnData.append(['    Status:', 'State: {} | Reason: {}'
                                  .format(value['status']['state'], value['status']['reason'])])

                unknown = []
                filtered = []

                if 'tcp' in value:

                    returnData.append(['    TCP:', ''])

                    for y, z in value['tcp'].items():

                        if z['state'] == 'unknown':
                            unknown.append(z['name'] + ' (' + str(y) + ')')
                            continue

                        if z['state'] == 'filtered':
                            unknown.append(z['name'] + ' (' + str(y) + ')')
                            continue

                        props = 'State: ' + z['state'] + ' | Reason: ' + z['reason']

                        if z['product'] != '':
                            props += ' | Product: ' + z['product']

                        returnData.append(['        Port ' + str(y) + ' (' + z['name'] + ')', props])
                        # returnData.append(['            Version:', z['version']])
                        # returnData.append(['            Extra Info:', z['extrainfo']])
                        # returnData.append(['            Conf:', z['conf']])
                        # returnData.append(['            Cpe:', z['cpe']])

                    returnData.append(['', ''])

                if len(filtered)>0:
                    currentLine = ''
                    for a in range(len(filtered)):
                        currentLine += filtered[a]
                        if a%5 == 0:
                            returnData.append(['    Filtered State Ports', currentLine])
                            currentLine = ''
                    returnData.append(['    Filtered State Ports', currentLine])
                    returnData.append(['', ''])

                if len(unknown)>0:
                    returnData.append(['    Unknown State Ports', len(unknown)])
                    returnData.append(['', ''])


        # Google IP for tests: 172.217.29

        return returnData


