import time


class Logger:

    __TAG = 'Logger'
    __history = []
    __header = ['SRC', 'MODULE', 'TIME', 'MESSAGE']
    __initialized = False

    def __init__(self, tag):
        self.tag = tag
        if not type(self).__initialized:
            type(self).__initialized = True
            new_entry = [
                'LOCAL',
                type(self).__TAG,
                time.strftime("%d.%m.%y %H:%M:%S"),
                'Orange System Profiler initialized.'
            ]
            type(self).__history.insert(0, new_entry)

    def log(self, msg):
        new_entry = [
                'LOCAL',
                self.tag,
                time.strftime("%d.%m.%y %H:%M:%S"),
                msg
            ]
        type(self).__history.insert(0, new_entry)

    @classmethod
    def getLog(cls, filter = '', max_length = 65):
        filter = filter.split()
        return_data = []
        return_data.append(cls.__header)
        if len(cls.__history) == 0: return return_data
        for log in cls.__history:
            if len(log[3])>max_length: log[3] = log[3][:max_length-3] + '...'
            if len(filter)>0:
                for y in log:
                    if any(i in y for i in filter):
                        return_data.append(log)
                        break
            else:
                return_data.append(log)
        return return_data


