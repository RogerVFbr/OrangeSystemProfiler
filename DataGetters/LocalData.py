import os, psutil, platform, cpuinfo, socket, ipaddress
import time, threading

from DataGetters.SubnetFinder import SubnetFinder


class LocalData:

    __TAG = 'LocalData: '
    __cpuInfo = cpuinfo.get_cpu_info()
    __processes = {'last_fetch': 0, 'content': []}
    __processesNetworkUsage = {'last_fetch': 0, 'content': {}}
    __networkInfo = {'last_fetch': 0, 'domain_name': '', 'ip': '', 'netmask': ''}
    __snf = SubnetFinder()

    def __init__(self):
        pass

    #  ==========================================================================================================
    #                                                   GETTERS
    #  ==========================================================================================================

    def test(self): print('testeeeeeee')

    def getCpuFreq(self): return psutil.cpu_freq()

    def getCpuPercentage(self): return psutil.cpu_percent()

    def getCores(self): return psutil.cpu_count()

    def getPerCoreUsage(self): return psutil.cpu_percent(percpu=True)

    def getPhysicalCores(self): return psutil.cpu_count(logical=False)

    def getVirtualMemory(self): return psutil.virtual_memory()

    def getProcessorInfo(self): return platform.processor()

    def getNetworkName(self): return platform.node()

    def getSystemVersion(self): return platform.platform()

    def getSystemType(self): return platform.system()

    def getDiskUsage(self): return psutil.disk_usage('.')

    def getNetworkInfo(self):

        try:
            addrs = psutil.net_if_addrs()
        except Exception as error:
            addrs = {}

        try:
            stats = psutil.net_if_stats()
        except Exception as error:
            stats = {}

        try:
            counters = psutil.net_io_counters(pernic=True)
        except Exception as error:
            counters = {}

        return [addrs, stats, counters]

    def getProcessorArchitecture(self):
        if 'arch' in type(self).__cpuInfo:
            return type(self).__cpuInfo['arch']
        else:
            return ''

    def getProcessorBrand(self):
        if 'brand' in type(self).__cpuInfo:
            return type(self).__cpuInfo['brand']
        else:
            return ''

    def getProcessorWordLength(self):
        if 'bits' in type(self).__cpuInfo:
            return type(self).__cpuInfo['bits']
        else:
            return ''

    def getProcessorActualSpeed(self): return type(self).__cpuInfo['hz_actual']

    def getProcessorL2Size(self):
        if 'l2_cache_size' in type(self).__cpuInfo:
            return type(self).__cpuInfo['l2_cache_size']
        else:
            return ''

    def getProcessorL2Line(self):
        if 'l2_cache_line_size' in type(self).__cpuInfo:
            return type(self).__cpuInfo['l2_cache_line_size']
        else:
            return ''

    def getProcessorL2Assoc(self):
        if 'l2_cache_associativity' in type(self).__cpuInfo:
            return type(self).__cpuInfo['l2_cache_associativity']
        else:
            return ''

    def getProcesses(self):
        time_now = time.time()
        if time_now - type(self).__processes['last_fetch'] > 1:
            type(self).__processes['last_fetch'] = time_now
            t = threading.Thread(target=type(self).__updateProcesses)
            t.start()
        return type(self).__processes['content']

    def getProcessesNetworkUsage(self):
        time_now = time.time()
        if time_now - type(self).__processesNetworkUsage['last_fetch'] > 2:
            type(self).__processesNetworkUsage['last_fetch'] = time_now
            t = threading.Thread(target=type(self).__updateProcessesNetworkUsage)
            t.start()
        return type(self).__processesNetworkUsage['content']

    def getCurrentWorkingDirectory(self): return os.getcwd()

    def getFilesAndFoldersOnPath(self, path):

        foldersList, filesList = [], []

        if os.path.isdir(path):
            itemsList = os.listdir(path.strip())
            for i in itemsList:
                p = os.path.join(path.strip(), i)
                if os.path.isfile(p):
                    filesList.append({
                        'name': i,
                        'size': os.stat(p).st_size,
                        'accessed': os.stat(p).st_atime,
                        'modified': os.stat(p).st_ctime
                    })

                elif os.path.isdir(p):
                    foldersList.append({
                        'name': i
                    })

        foldersList.sort(key=lambda x: x['name'])
        filesList.sort(key=lambda x: x['name'])

        return [foldersList, filesList]

    def updateHosts(self, path): type(self).__snf.updateHosts(path)

    def getHosts(self): return type(self).__snf.getHosts()

    def getDomainName(self):
        time_now = time.time()
        if time_now - type(self).__networkInfo['last_fetch'] > 3:
            type(self).__networkInfo['last_fetch'] = time_now
            t = threading.Thread(target=type(self).__updateNetworkInfo)
            t.start()
        return type(self).__networkInfo['domain_name']

    def getIp(self):
        time_now = time.time()
        if time_now - type(self).__networkInfo['last_fetch'] > 2:
            type(self).__networkInfo['last_fetch'] = time_now
            t = threading.Thread(target=type(self).__updateNetworkInfo)
            t.start()
        return type(self).__networkInfo['ip']

    def getNetmask(self):
        time_now = time.time()
        if time_now - type(self).__networkInfo['last_fetch'] > 2:
            type(self).__networkInfo['last_fetch'] = time_now
            t = threading.Thread(target=type(self).__updateNetworkInfo)
            t.start()
        return type(self).__networkInfo['netmask']

    #  ==========================================================================================================
    #                                                UPDATERS
    #  ==========================================================================================================

    @classmethod
    def __updateProcessesNetworkUsage(cls):
        networkUsage = {}
        data = psutil.process_iter(attrs=['pid'])
        for z in data:
            try:
                p = psutil.Process(z.info['pid'])
                networkUsage[z.info['pid']] = p.connections()
            except Exception as error:
                print(error)
                continue

        cls.__processesNetworkUsage['content'] = networkUsage

    @classmethod
    def __updateProcesses(cls):
        cls.__processes['content'] = [x.info for x in psutil.process_iter(attrs=['pid', 'name', 'username', 'exe',
                                                           'cpu_times', 'cpu_percent', 'memory_percent',
                                                           'memory_info', 'num_threads'])]

    @classmethod
    def __updateNetworkInfo(cls):
        try:
            cls.__networkInfo['domain_name'] = socket.getfqdn()
            cls.__networkInfo['ip'] = socket.gethostbyname(socket.getfqdn())
            cls.__networkInfo['netmask'] = ipaddress.ip_network(cls.__networkInfo['ip']).netmask
        except:
            pass









