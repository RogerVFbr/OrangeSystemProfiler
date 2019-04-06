import os
import platform
import subprocess
import threading, multiprocessing
import copy
import time
from nmap import PortScanner


class SubnetFinder:

    __TAG = 'SubnetFinder: '
    __data = {'current': 0}
    __attributes = {
        'status': '',
        'ip': '',
        'starttime': 0,
        'finishtime': 0,
        'details': '',
        'valid_hosts': [],
        'host_details': {}
    }

    __ping_args = []
    __workerThreads = []

    def __init__(self):

        if platform.system() == "Windows":
            type(self).__ping_args = ["ping", "-n", "1", "-l", "1", "-w", "100"]

        else:
            type(self).__ping_args = ['ping', '-c', '1', '-W', '1']

    def getHosts(self):
        if type(self).__data['current'] == 0:
            return type(self).__attributes
        return type(self).__data[type(self).__data['current']]

    def updateHosts(self, base_ip):

        fetch_id = time.time()
        type(self).__data[fetch_id] = copy.copy(type(self).__attributes)
        type(self).__data['current'] = fetch_id

        # Validate input
        is_input_valid = True
        base_ip = base_ip.split('.')
        if len(base_ip) >= 3:
            for x in base_ip:
                if len(x) > 3:
                    is_input_valid = False
                    break
                try:
                    _ = int(x)
                except:
                    is_input_valid = False
                    break
        else:
            is_input_valid = False

        # If input invalid, inform hosts object and interrupt
        if not is_input_valid:
            type(self).__data[fetch_id]['status'] = 'invalid'
            return

        # Input is valid, update currentHosts object
        type(self).__data[fetch_id]['status'] = 'fetching'
        type(self).__data[fetch_id]['ip'] = '.'.join(base_ip[:3])
        type(self).__data[fetch_id]['starttime'] = time.time()
        type(self).__data[fetch_id]['host_details'] = {}

        # Start analysis on separate thread
        t = threading.Thread(target=self.__findHosts, args=[fetch_id])
        t.daemon = True
        t.start()

    def __findHosts(self, fetch_id):

        host_validos = []
        base_ip = type(self).__data[fetch_id]['ip']

        # Check for subnets
        for i in range(1, 255):
            ip_test = base_ip + '.{}'.format(i)
            type(self).__data[fetch_id]['details'] = 'Testing: ' + ip_test
            ping_code = subprocess.call(type(self).__ping_args + [ip_test],
                                  stdout=open(os.devnull, 'w'),
                                  stderr=open(os.devnull, 'w'))

            if fetch_id != type(self).__data['current']:
                return

            if ping_code == 0:
                host_validos.append(ip_test)

        # Update hosts object with aqcuired data
        type(self).__data[fetch_id]['status'] = 'fetching_details'
        type(self).__data[fetch_id]['valid_hosts'] = host_validos

        # Summon portscanner worker threads
        no_of_workers = 20
        q = multiprocessing.Queue()
        for x in range(len(type(self).__data[fetch_id]['valid_hosts'])):
            if fetch_id != type(self).__data['current']: return
            ip = type(self).__data[fetch_id]['valid_hosts'][x]
            type(self).__data[fetch_id]['details'] = 'Analyzing: ' + ip
            t = multiprocessing.Process(target=self.__portscannerWorkerThreads, args=(fetch_id, ip, x, q))
            t.daemon = True
            t.start()
            type(self).__workerThreads.append(t)
            if len(type(self).__workerThreads) == no_of_workers:
                type(self).__data[fetch_id]['details'] = 'Analyzing batch {} - {} '\
                    .format(x+1-len(type(self).__workerThreads), x+1)
                no_of_returns = 0
                while no_of_returns < no_of_workers:
                    data = q.get()
                    type(self).__data[fetch_id]['host_details'][data.keys()[0]] = data[data.keys()[0]]
                    no_of_returns += 1
                for y in type(self).__workerThreads:
                    y.join()
                type(self).__workerThreads = []
                type(self).__data[fetch_id]['host_details'] = \
                    self.reorderDictByNumericKey(type(self).__data[fetch_id]['host_details'], 'key')
                # print('{} PortScanner batch ready'.format(x+1))

        # Deal with remaining portscanner worker threads
        type(self).__data[fetch_id]['details'] = 'Analyzing batch {} - {} ' \
            .format(len(type(self).__data[fetch_id]['valid_hosts'])
                    - len(type(self).__workerThreads), len(type(self).__data[fetch_id]['valid_hosts']))
        for y in type(self).__workerThreads:
            y.join()
        type(self).__workerThreads = []
        type(self).__data[fetch_id]['host_details'] = \
            self.reorderDictByNumericKey(type(self).__data[fetch_id]['host_details'], 'key')
        # print('PortScanner finished')

        # Update hosts object with finished status
        type(self).__data[fetch_id]['status'] = 'ready'
        type(self).__data[fetch_id]['finishtime'] = time.time()

    def __portscannerWorkerThreads(self, fetch_id, ip, no, q):
        nm = PortScanner()
        # type(self).__data[fetch_id]['details'] = 'Analyzing: ' + str(ip)
        elapsed_start = time.time()
        nm.scan(ip)
        if fetch_id != type(self).__data['current']:
            return
        try:
            data = nm[ip]
            elapsed = time.time() - elapsed_start
            q.put({ip: {**data, **{'elapsed': elapsed}}})

        except:
            pass

    def reorderDictByNumericKey(self, dct, key):
        odlist = [{'key': k, 'value': v} for k, v in dct.items()]
        odlist = sorted(odlist, key=lambda k: int(str(k[key]).replace('.', '')))
        return {x['key']: x['value'] for x in odlist}







