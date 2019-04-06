import os
import platform
import subprocess
import threading
import copy
import time
from nmap import PortScanner

from DataGetters.Logger import Logger


class SubnetFinder:

    __TAG = 'SubnetFinder'
    __lg = Logger(__TAG)
    __data = { 'current': 0 }
    __attributes = {
        'status': '',
        'ip': '',
        'starttime': 0,
        'finishtime': 0,
        'details': '',
        'valid_hosts': [],
        'hosts_to_scan': [],
        'host_details': {},
        'avg_scan_time': 0,
        'no_of_workers': 0
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
        type(self).__lg.log('Initializing new scan @ {}'.format('.'.join(base_ip[:3])))
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
                type(self).__lg.log('Active IP found @ {}'.format(ip_test))
                host_validos.append(ip_test)

        # Update hosts object with aqcuired data
        type(self).__data[fetch_id]['status'] = 'fetching_details'
        type(self).__data[fetch_id]['valid_hosts'] = host_validos
        type(self).__data[fetch_id]['hosts_to_scan'] = host_validos[:]

        # Calculate and update number of worker threads
        max_no_of_workers = 4
        no_of_hosts = len(type(self).__data[fetch_id]['hosts_to_scan'])
        no_of_workers = max_no_of_workers if max_no_of_workers<no_of_hosts else no_of_hosts
        type(self).__data[fetch_id]['no_of_workers'] = no_of_workers

        # Fire worker threads
        lock = threading.Lock()
        fire_worker_threads_message = 'Firing {} worker threads. IPs found: {}'\
                .format(no_of_workers, no_of_hosts)
        type(self).__data[fetch_id]['details'] = fire_worker_threads_message
        type(self).__lg.log(fire_worker_threads_message)

        for x in range(no_of_workers):
            t = threading.Thread(target=self.__portscannerWorkerThreads, args=(fetch_id, lock))
            t.daemon = True
            t.start()
            type(self).__workerThreads.append(t)
        for y in type(self).__workerThreads:
            y.join()

        if fetch_id != type(self).__data['current']: return

        # Update hosts object with finished status
        scan_times = [v['elapsed'] for k, v in type(self).__data[fetch_id]['host_details'].items()]
        type(self).__data[fetch_id]['avg_scan_time'] = sum(scan_times) / len(scan_times)
        type(self).__data[fetch_id]['status'] = 'ready'
        type(self).__data[fetch_id]['finishtime'] = time.time()

    def __portscannerWorkerThreads(self, fetch_id, lock):
        nm = PortScanner()
        while len(type(self).__data[fetch_id]['hosts_to_scan'])>0:
            elapsed_start = time.time()
            lock.acquire()
            if len(type(self).__data[fetch_id]['hosts_to_scan']) == 0: break
            try:
                ip = type(self).__data[fetch_id]['hosts_to_scan'][0]
                type(self).__data[fetch_id]['hosts_to_scan'].remove(ip)
            finally:
                lock.release()
            nm.scan(ip)
            if fetch_id != type(self).__data['current']:
                return
            try:
                type(self).__data[fetch_id]['host_details'][ip] = nm[ip]
                type(self).__data[fetch_id]['host_details'][ip]['elapsed'] = time.time() - elapsed_start

            except:
                continue

            lock.acquire()
            try:
                type(self).__data[fetch_id]['host_details'] = \
                    self.reorderDictByNumericKey(type(self).__data[fetch_id]['host_details'], 'key')
                type(self).__data[fetch_id]['details'] = 'Progress: {} / {}'.format(
                    len(type(self).__data[fetch_id]['host_details']),
                    len(type(self).__data[fetch_id]['valid_hosts'])
                )
            finally:
                type(self).__lg.log('Finished scanning ports @ {}'.format(ip))

                lock.release()

    def reorderDictByNumericKey(self, dct, key):
        odlist = [{'key': k, 'value': v} for k, v in dct.items()]
        odlist = sorted(odlist, key=lambda k: int(str(k[key]).replace('.', '')))
        return {x['key']: x['value'] for x in odlist}







