from DataGetters.Broadcaster import Broadcaster
from DataGetters.LocalData import LocalData
from DataGetters.RemoteData import RemoteData
from DataGetters.Logger import Logger



class DataGetters:

    __TAG = 'DataGetters'
    __ds = LocalData()
    __bc = Broadcaster()
    __lg = Logger(__TAG)

    #  ==========================================================================================================
    #                                                DATA GETTERS
    #  ==========================================================================================================

    @classmethod
    def getCpuFreq(cls): return cls.__ds.getCpuFreq()

    @classmethod
    def getCpuPercentage(cls): return cls.__ds.getCpuPercentage()

    @classmethod
    def getCores(cls): return cls.__ds.getCores()

    @classmethod
    def getPerCoreUsage(cls): return cls.__ds.getPerCoreUsage()

    @classmethod
    def getPhysicalCores(cls): return cls.__ds.getPhysicalCores()

    @classmethod
    def getVirtualMemory(cls): return cls.__ds.getVirtualMemory()

    @classmethod
    def getProcessorInfo(cls): return cls.__ds.getProcessorInfo()

    @classmethod
    def getNetworkName(cls): return cls.__ds.getNetworkName()

    @classmethod
    def getSystemVersion(cls): return cls.__ds.getSystemVersion()

    @classmethod
    def getSystemType(cls): return cls.__ds.getSystemType()

    @classmethod
    def getDiskUsage(cls): return cls.__ds.getDiskUsage()

    @classmethod
    def getNetworkInfo(cls): return cls.__ds.getNetworkInfo()

    @classmethod
    def getProcessorArchitecture(cls): return cls.__ds.getProcessorArchitecture()

    @classmethod
    def getProcessorBrand(cls): return cls.__ds.getProcessorBrand()

    @classmethod
    def getProcessorWordLength(cls): return cls.__ds.getProcessorWordLength()

    @classmethod
    def getProcessorActualSpeed(cls): return cls.__ds.getProcessorActualSpeed()

    @classmethod
    def getProcessorL2Size(cls): return cls.__ds.getProcessorL2Size()

    @classmethod
    def getProcessorL2Line(cls): return cls.__ds.getProcessorL2Line()

    @classmethod
    def getProcessorL2Assoc(cls): return cls.__ds.getProcessorL2Assoc()

    @classmethod
    def getProcesses(cls): return cls.__ds.getProcesses()

    @classmethod
    def getProcessesNetworkUsage(cls): return cls.__ds.getProcessesNetworkUsage()

    @classmethod
    def getCurrentWorkingDirectory(cls): return cls.__ds.getCurrentWorkingDirectory()

    @classmethod
    def getFilesAndFoldersOnPath(cls, path): return cls.__ds.getFilesAndFoldersOnPath(path)

    @classmethod
    def getDomainName(cls): return cls.__ds.getDomainName()

    @classmethod
    def getIp(cls): return cls.__ds.getIp()

    @classmethod
    def getNetmask(cls): return cls.__ds.getNetmask()

    #  ==========================================================================================================
    #                                                 SUBNET FINDER
    #  ==========================================================================================================

    @classmethod
    def updateHosts(cls, path):
        cls.__lg.log('Updating SubnetFinder hosts @ {}'.format(path))
        cls.__ds.updateHosts(path)

    @classmethod
    def getHosts(cls): return cls.__ds.getHosts()

    #  ==========================================================================================================
    #                                          STATE CONTROLLERS AND READERS
    #  ==========================================================================================================

    @classmethod
    def setLocalData(cls):
        if isinstance(cls.__ds, RemoteData):
            del cls.__ds
            cls.__ds = LocalData()
            cls.__lg.log('Data gathering set to local.')

    @classmethod
    def setRemoteData(cls, hostPort):
        cls.__ds = RemoteData(hostPort)
        cls.__lg.log('Data gathering set to remote.')

    @classmethod
    def isLocal(cls):
        if isinstance(cls.__ds, LocalData):
            return True
        return False

    @classmethod
    def isRemote(cls):
        if isinstance(cls.__ds, RemoteData):
            return True
        return False

