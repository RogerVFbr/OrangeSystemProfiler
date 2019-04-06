import socket
from collections import namedtuple
from collections import OrderedDict

class Helpers:

    __odnt = {}

    @classmethod
    def convertBytesToGigabytes(self, amount):
        return round(amount/(1024*1024*1024), 2)

    @classmethod
    def convertBytesToMegabytes(self, amount):
        return round(amount / (1024 * 1024), 2)

    @classmethod
    def convertBytesToKilobytes(self, amount):
        return round(amount / (1024), 2)

    @classmethod
    def limitFileNameLength(cls, filename, maxsize):
        length = len(filename)

        if length <= maxsize:
            return filename

        else:
            splitname = filename.split('.')
            extension = '.' + splitname[len(splitname)-1]
            returnName = ''
            charIndex = 0

            while (len(returnName)+len(extension)+5)<maxsize:
                returnName += filename[charIndex]
                charIndex += 1

            returnName += '(...)' + extension

            return returnName

    @classmethod
    def convertSecsToHHMMSS(cls, ns):
        # ns = int(ns)
        secs = int(ns%60)
        mins = int(ns//60)
        hours = int(ns//60//60)

        if hours>0:
            return '{}h {}m {}s'.format(hours, mins, secs)

        if mins>0:
            return '{}m {}s'.format(mins, secs)

        return '{}s'.format(secs)

    @classmethod
    def convertFamilyToAddType(cls, data):

        if data == socket.AF_INET6 or 'AF_INET6' in str(data):
            return 'IPv6'

        elif data == socket.AF_INET or 'AF_INET' in str(data):
            return 'IPv4'

        # elif data == socket.AF_UNIX:
        #     return 'Unix'

        elif 'AF_LINK' in str(data):
            return 'AF_LINK'
        else:
            return '-'

    @classmethod
    def convertToSocketType(cls, data):
        if data == socket.SOCK_STREAM: return 'TCP'
        elif data == socket.SOCK_DGRAM: return 'UDP'
        elif data == socket.SOCK_RAW: return 'IP'
        else: return '-'

    @classmethod
    def isNamedtupleInstance(cls, x):
        t = type(x)
        b = t.__bases__
        if len(b) != 1 or b[0] != tuple: return False
        f = getattr(t, '_fields', None)
        if not isinstance(f, tuple): return False
        return all(type(n) == str for n in f)

    @classmethod
    def convertNamedtuplesToOrderedDicts(cls, data):

        # Also treats AF_LINK family value, unexistent in win

        if cls.isNamedtupleInstance(data):
            data = data._asdict()
            data = cls.convertNamedtuplesToOrderedDicts(data)

        elif isinstance(data, (dict, OrderedDict)):
            for k, v in data.items():
                if k == 'family' and 'AF_LINK' in str(v):
                    data[k] = str(v)
                data[k] = cls.convertNamedtuplesToOrderedDicts(v)

        elif isinstance(data, list):
            for x in range(len(data)):
                data[x] = cls.convertNamedtuplesToOrderedDicts(data[x])

        elif isinstance(data, tuple) and not cls.isNamedtupleInstance(data):
            data = list(data)
            data = cls.convertNamedtuplesToOrderedDicts(data)
            data = tuple(data)

        return data

    @classmethod
    def convertOrderedDictsToNamedtuples(cls, data):

        if isinstance(data, (dict, OrderedDict)):
            for k, v in data.items():
                data[k] = cls.convertOrderedDictsToNamedtuples(v)
            if isinstance(data, OrderedDict):
                keys = ''.join([*data])
                if keys not in cls.__odnt:
                    cls.__odnt[keys] = namedtuple('transfernt', data.keys())
                data = cls.__odnt[keys](**data)

        elif isinstance(data, list):
            for x in range(len(data)):
                data[x] = cls.convertOrderedDictsToNamedtuples(data[x])

        elif isinstance(data, tuple) and not cls.isNamedtupleInstance(data):
            data = list(data)
            data = cls.convertOrderedDictsToNamedtuples(data)
            data = tuple(data)

        return data

    @classmethod
    def decodeNICactivity(cls, state):
        if state:
            return 'Active'
        return 'Inactive'

    @classmethod
    def decodeNICcomType(cls, ty):
        if 'DUPLEX_FULL' in str(ty):
            return 'full-duplex'
        elif 'DUPLEX_HALF' in str(ty):
            return 'half-duplex'
        elif 'DUPLEX_UNKNOWN' in str(ty):
            return 'unknown comm. type'
        return ty

