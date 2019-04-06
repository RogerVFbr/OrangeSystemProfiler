import os, platform, subprocess, threading, multiprocessing
import copy, time
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
    __com_struct = {
        'header': '',
        'info': '',
        'payload': None
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

        # Calculate and update number of worker processes
        max_no_of_workers = 4
        no_of_hosts = len(type(self).__data[fetch_id]['hosts_to_scan'])
        no_of_workers = max_no_of_workers if max_no_of_workers<no_of_hosts else no_of_hosts
        type(self).__data[fetch_id]['no_of_workers'] = no_of_workers

        # Fire worker processes
        fire_worker_threads_message = 'Firing {} worker processes. IPs found: {}'\
                .format(no_of_workers, no_of_hosts)
        type(self).__data[fetch_id]['details'] = fire_worker_threads_message
        type(self).__lg.log(fire_worker_threads_message)
        main_sub_q = multiprocessing.Queue()
        sub_main_q = multiprocessing.Queue()
        lock = multiprocessing.Lock()
        for x in range(no_of_workers):
            p = multiprocessing.Process(target=self.portscannerWorkerProcess,
                                          args=[main_sub_q, sub_main_q, lock])
            p.daemon = True
            p.start()
            type(self).__workerThreads.append(p)

        # Establish communications with worker processes
        finished_processes = 0
        while finished_processes<no_of_workers:
            received_data = sub_main_q.get()
            if received_data['header'] == 'result':
                type(self).__data[fetch_id]['host_details'][received_data['info']] = received_data['payload']
                type(self).__data[fetch_id]['host_details'] = \
                    self.reorderDictByNumericKey(type(self).__data[fetch_id]['host_details'], 'key')
                type(self).__data[fetch_id]['details'] = 'Progress: {} / {}'.format(
                    len(type(self).__data[fetch_id]['host_details']),
                    len(type(self).__data[fetch_id]['valid_hosts'])
                )
                type(self).__lg.log('Finished scanning ports @ {}'.format(received_data['info']))

            elif received_data['header'] == 'error':
                type(self).__lg.log('Error', str(received_data))

            # Feed new IP to worker process or terminate
            if fetch_id != type(self).__data['current'] or \
                    len(type(self).__data[fetch_id]['hosts_to_scan']) == 0:
                finished_processes += 1
                main_sub_q.put({
                    'header': 'terminate',
                    'info': '',
                    'payload': ''
                })
                type(self).__lg.log('Terminating process {}/{}'.format(finished_processes, no_of_workers))

            else:
                return_data = type(self).__data[fetch_id]['hosts_to_scan'][0]
                type(self).__data[fetch_id]['hosts_to_scan'].remove(return_data)
                main_sub_q.put({
                    'header': 'ip',
                    'info': '',
                    'payload': return_data
                })
        for y in type(self).__workerThreads:
            y.join()

        if fetch_id != type(self).__data['current']: return

        # Update hosts object with finished status
        scan_times = [v['elapsed'] for k, v in type(self).__data[fetch_id]['host_details'].items()]
        if len(scan_times) != 0:
            type(self).__data[fetch_id]['avg_scan_time'] = sum(scan_times) / len(scan_times)
        type(self).__data[fetch_id]['status'] = 'ready'
        type(self).__data[fetch_id]['finishtime'] = time.time()

    def portscannerWorkerProcess(self, mainSubQ, subMainQ, lock):
        nm = PortScanner()
        return_data = {
            'header': 'initialize',
            'info': '',
            'payload': ''
        }
        while True:
            elapsed_start = time.time()
            lock.acquire()
            try:
                print()
                subMainQ.put(return_data)
                instructions = None
                while instructions is None:
                    instructions = mainSubQ.get()
            finally:
                lock.release()
            if instructions['header'] == 'terminate': return
            ip = instructions['payload']
            nm.scan(ip)
            try:
                return_data['header'] = 'result'
                return_data['info'] = ip
                return_data['payload'] = {**nm[ip], **{'elapsed': time.time() - elapsed_start}}
            except Exception as error:
                return_data['header'] = 'error'
                return_data['info'] = ip
                return_data['payload'] = str(error)


    def reorderDictByNumericKey(self, dct, key):
        odlist = [{'key': k, 'value': v} for k, v in dct.items()]
        odlist = sorted(odlist, key=lambda k: int(str(k[key]).replace('.', '')))
        return {x['key']: x['value'] for x in odlist}







