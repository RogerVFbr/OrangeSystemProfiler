import socket
import time
import threading
import pickle
import copy

from DataGetters.Logger import Logger
from Helpers.Helpers import Helpers as hl


class RemoteData:

    __TAG = 'RemoteData'
    __processesNetworkUsage = { 'fetch_data': False }
    __thread = None
    __isActive = False
    __message = 'Remote data gathering disabled.'
    __hostPort = ['', None]
    __lg = Logger(__TAG)

    __remoteDataStructure = dict(
        getCpuFreq={'fetch': False, 'status': 'idle', 'content': ''},
        getCpuPercentage={'fetch': False, 'status': 'idle', 'content': 0},
        getCores={'fetch': False, 'status': 'idle', 'content': ''},
        getPerCoreUsage={'fetch': False, 'status': 'idle', 'content': ''},
        getPhysicalCores={'fetch': False, 'status': 'idle', 'content': ''},
        getVirtualMemory={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorInfo={'fetch': False, 'status': 'idle', 'content': ''},
        getNetworkName={'fetch': False, 'status': 'idle', 'content': ''},
        getSystemVersion={'fetch': False, 'status': 'idle', 'content': ''},
        getSystemType={'fetch': False, 'status': 'idle', 'content': ''},
        getDiskUsage={'fetch': False, 'status': 'idle', 'content': ''},
        getNetworkInfo={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorArchitecture={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorBrand={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorWordLength={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorActualSpeed={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorL2Size={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorL2Line={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessorL2Assoc={'fetch': False, 'status': 'idle', 'content': ''},
        getProcesses={'fetch': False, 'status': 'idle', 'content': ''},
        getProcessesNetworkUsage={'fetch': False, 'status': 'idle', 'content': ''},
        getCurrentWorkingDirectory={'fetch': False, 'status': 'idle', 'content': ''},
        getFilesAndFoldersOnPath={'fetch': False, 'status': 'idle', 'content': '', 'args': ''},
        updateHosts={'fetch': False, 'status': 'idle', 'content': '', 'args': ''},
        getHosts={'fetch': False, 'status': 'idle', 'content': ''},
        getDomainName={'fetch': False, 'status': 'idle', 'content': ''},
        getIp={'fetch': False, 'status': 'idle', 'content': ''},
        getNetmask={'fetch': False, 'status': 'idle', 'content': ''},
    )

    __remoteData = None
    __connectionErrorCount = {'count': 0, 'max': 3}

    #  ==========================================================================================================
    #                                          CONSTRUCTOR / DESCTRUCTOR
    #  ==========================================================================================================

    def __init__(self, hostPort):
        self.__initializeRemoteData()
        type(self).__isActive = True
        type(self).__hostPort[0] = hostPort[0]

        try:
            type(self).__hostPort[1] = int(hostPort[1])
        except:
            pass

        if type(self).__thread is None:
            type(self).__lg.log('Initializing RemoteData module thread.')
            type(self).__thread = threading.Thread(target=type(self).__updateRemoteData)
            type(self).__thread.daemon = True
            type(self).__thread.start()

    def __del__(self):
        type(self).__initializeRemoteData()
        type(self).__isActive = False
        type(self).__lg.log('Shuting down RemoteData module.')


    #  ==========================================================================================================
    #                                                   GETTERS
    #  ==========================================================================================================

    def getCpuFreq(self): return self.__request('getCpuFreq')

    def getCpuPercentage(self): return self.__request('getCpuPercentage')

    def getCores(self): return self.__request('getCores')

    def getPerCoreUsage(self): return self.__request('getPerCoreUsage')

    def getPhysicalCores(self): return self.__request('getPhysicalCores')

    def getVirtualMemory(self): return self.__request('getVirtualMemory')

    def getProcessorInfo(self): return self.__request('getProcessorInfo')

    def getNetworkName(self): return self.__request('getNetworkName')

    def getSystemVersion(self): return self.__request('getSystemVersion')

    def getSystemType(self): return self.__request('getSystemType')

    def getDiskUsage(self): return self.__request('getDiskUsage')

    def getNetworkInfo(self): return self.__request('getNetworkInfo')

    def getProcessorArchitecture(self): return self.__request('getProcessorArchitecture')

    def getProcessorBrand(self): return self.__request('getProcessorBrand')

    def getProcessorWordLength(self): return self.__request('getProcessorWordLength')

    def getProcessorActualSpeed(self): return self.__request('getProcessorActualSpeed')

    def getProcessorL2Size(self): return self.__request('getProcessorL2Size')

    def getProcessorL2Line(self): return self.__request('getProcessorL2Line')

    def getProcessorL2Assoc(self): return self.__request('getProcessorL2Assoc')

    def getProcesses(self): return self.__request('getProcesses')

    def getProcessesNetworkUsage(self): return self.__request('getProcessesNetworkUsage')

    def getCurrentWorkingDirectory(self): return self.__request('getCurrentWorkingDirectory')

    def getFilesAndFoldersOnPath(self, path):
        type(self).__remoteData['getFilesAndFoldersOnPath']['args'] = path
        return self.__request('getFilesAndFoldersOnPath')

    def updateHosts(self, path):
        type(self).__remoteData['updateHosts']['args'] = path
        self.__request('updateHosts')

    def getHosts(self): return self.__request('getHosts')

    def getDomainName(self): return self.__request('getDomainName')

    def getIp(self): return self.__request('getIp')

    def getNetmask(self): return self.__request('getNetmask')

    def __request(self, method):
        type(self).__remoteData[method]['fetch'] = True
        return type(self).__remoteData[method]['content']

    #  ==========================================================================================================
    #                                                UPDATERS
    #  ==========================================================================================================

    @classmethod
    def __updateRemoteData(cls):

        while True:

            # If user is monitoring locally, restart the loop
            if not cls.__isActive:
                cls.__setMessage('Remote data gathering disabled.')
                time.sleep(1)
                continue

            cls.__setMessage('Remote data gathering enabled.')
            cls.__lg.log('Remote data gathering enabled.')

            host, port = '', 0

            # Checks for validity of user inputs and treats accordingly
            if isinstance(cls.__hostPort[0], str) and cls.__hostPort[0] != '':
                host = cls.__hostPort[0]
            else:
                host = socket.gethostname()

            if isinstance(cls.__hostPort[1], int):
                port = cls.__hostPort[1]
            else:
                port = 9999

            # Main communication loop
            while True:

                if not cls.__isActive: break

                requests = []

                # Build requests list
                for k, v in cls.__remoteData.items():
                    if v['fetch'] == False: continue
                    if 'args' in v:
                        requests.append((k, v['args']))
                    else:
                        requests.append(k)

                # If requests list is empty, no requests at the moment, restart loop
                if len(requests) == 0:
                    cls.__setMessage('Data gathering enabled but no requests at this moment.')
                    time.sleep(1)
                    continue

                # Pickle serialize request
                request_bytes = pickle.dumps(requests)

                # Instantiate client socket
                cls.__setMessage('Instantiating socket...')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Attempts to communicate with server
                try:

                    cls.__setMessage('Attempting to connect to host {} port {}.'.format(host, port))
                    s.connect((host, port))
                    cls.__connectionErrorCount['count'] = 0
                    cls.__setMessage('Successfully connected to host {} port {}.'.format(host, port))
                    s.send(request_bytes)
                    response_bytes = s.recv(2000000)
                    cls.__setMessage('Successfully received response.')


                # If communication attempt fails
                except Exception as error:
                    a = str(error)
                    # print(a)
                    cls.__setMessage(a)
                    cls.__lg.log(a)
                    if 'WinError 10061' in str(error):
                        cls.__connectionErrorCount['count'] += 1
                        if cls.__connectionErrorCount['count'] == cls.__connectionErrorCount['max']:
                            cls.__setMessage('Unable to connect too many times, initializing data.')
                            cls.__lg.log('Unable to connect too many times, initializing data.')
                            cls.__initializeRemoteData()
                    s.close()
                    time.sleep(1)
                    continue

                # Attempts to pickle deserialize received data
                try:
                    cls.__setMessage('Attempting to decode response...')
                    response = pickle.loads(response_bytes, fix_imports=True)
                    response = hl.convertOrderedDictsToNamedtuples(response)

                # If pickle deserialize fails
                except Exception as error:
                    cls.__setMessage('Unable to decode response due to: ' + str(error))
                    cls.__lg.log('Unable to decode response due to: ' + str(error))
                    s.close()
                    if not cls.__isActive: break
                    time.sleep(1)
                    continue

                cls.__setMessage('Successfully decoded response from host {} : {}.'.format(host, port))
                cls.__lg.log('Successsfully acquired "{}" @ {} : {}.'.format('", "'.join(requests), host, port))

                s.close()

                # Feeds deserialized data to __remoteData dictionary
                for k, v in response.items():
                    cls.__remoteData[k]['fetch'] = False
                    cls.__remoteData[k]['content'] = v

                if not cls.__isActive:  break
                time.sleep(2)

    #  ==========================================================================================================
    #                                            AUXILIARY METHODS
    #  ==========================================================================================================

    @classmethod
    def __initializeRemoteData(cls):
        cls.__remoteData = copy.deepcopy(cls.__remoteDataStructure)

    @classmethod
    def __setMessage(cls, msg):
        cls.__message = msg

    @classmethod
    def getMessage(cls):
        return cls.__message






