import threading, socket, pickle, time
from DataGetters.Logger import Logger
from Helpers.Helpers import Helpers as hl
from DataGetters.LocalData import LocalData


class Broadcaster:

    __TAG = 'Broadcaster'
    __thread = None
    __ld = LocalData()
    __bdaddress = [socket.gethostname(), 9999, socket.gethostbyname(socket.gethostname())]
    __isBroadcasting = False
    __message = ''
    __lg = Logger(__TAG)

    def __init__(self):
        if type(self).__thread is None:
            type(self).__thread = threading.Thread(target=self.__processRequests)
            type(self).__thread.daemon = True
            type(self).__thread.start()

    def __processRequests(self):

        while True:

            # If Broadcasting is disabled, wait a second and restart loop
            if not type(self).__isBroadcasting:
                self.setMessage('Broadcasting disabled.')
                time.sleep(1)
                continue

            # Broadcasting just got enabled, instantiate socket
            type(self).__lg.log('Broadcasting enabled.')
            self.setMessage('Instantiating socket.')
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = socket.gethostname(), type(self).__bdaddress[1]

            # Checks for validity of user input and treats accordingly
            if type(port) != int:
                self.setMessage('Invalid user input, setting to default port 9999.')
                type(self).__lg.log('Invalid user input, setting to default port 9999.')
                port = 9999
                type(self).__bdaddress[1] = port

            # Attempt to bind host and port to socket
            while True:
                try:
                    self.setMessage('Attempting to bind...')
                    socket_server.bind((host, port))
                    self.setMessage('Successfully bound.')
                    type(self).__lg.log('Successfully bound @ {} : {}.'.format(host, port))

                    break
                except Exception as error:
                    self.setMessage('Could not bind due to' + str(error))
                    type(self).__lg.log('Could not bind due to' + str(error))

                    time.sleep(1)
                    if not type(self).__isBroadcasting: break

            # If user deactivated broadcasting, close socket and restart loop
            if not type(self).__isBroadcasting:
                self.setMessage('Broadcasting stopped. Closing server socket...')
                type(self).__lg.log('Broadcasting stopped. Closing server socket...')
                socket_server.close()
                continue

            # Start to listen for requests on given port
            socket_server.listen()

            # Main communication loop
            while True:

                # Awaiting and accepting incoming client request
                self.setMessage('Awaiting client request.')

                socket_client, addr = socket_server.accept()
                self.setMessage('Accepted connection from client at {}.'.format(str(addr)))

                # Receive client request data
                requests_raw = socket_client.recv(1024)
                self.setMessage('Received requests from {}.'.format(str(addr)))

                # Check if broadcasting got disabled in the meantime
                if not type(self).__isBroadcasting:
                    socket_client.close()
                    break

                # Pickle deserialize and extract requests from raw data received
                requests = pickle.loads(requests_raw)

                # Fetch local data per requests
                return_data = self.__fetchData(requests)

                # Pickle serialize data to be sent to client
                return_data = pickle.dumps(return_data)

                # Send serialized data back to client and close client socket
                socket_client.send(return_data)
                self.setMessage('Data sent back to client @ {}.'.format(str(addr)))
                type(self).__lg.log('Request attended @ {}.'.format(str(addr)))
                socket_client.close()

            # Communication loop has been terminated, close server socket and restart loop
            self.setMessage('Closing server socket...')
            socket_server.close()

    def __fetchData(self, requests):

        returnDict = {}

        # Check requests on requests list
        for x in requests:

            # If request is a tuple, method parameters have been sent, use them on method execution
            if type(x) == tuple or type(x) == list:
                returnDict[x[0]] = getattr(type(self).__ld, x[0])(x[1])

            # Request is not a tuple, it will be a string, execute corresponding method
            else:
                returnDict[x] = getattr(type(self).__ld, x)()

        return hl.convertNamedtuplesToOrderedDicts(returnDict)

    @classmethod
    def getBroadcastAddress(cls):
        return cls.__bdaddress

    @classmethod
    def startBroadcasting(cls, port):
        cls.__isBroadcasting = True
        try:
            cls.__bdaddress[1] = int(port)
        except:
            cls.__bdaddress[1] = port

    @classmethod
    def stopBroadcasting(cls):
        cls.__message = 'Broadcasting disabled. Full shutdown of module on next request.'
        cls.__lg.log('Broadcasting disabled. Full shutdown of module on next request.')
        cls.__isBroadcasting = False

    def setMessage(self, msg):
        type(self).__message = msg

    @classmethod
    def getMessage(cls):
        return cls.__message
