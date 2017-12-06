import getopt
from config.params import *


class Params:
    def __init__(self, argv):
        self.__argv = argv
        self.__optlist, _ = getopt.getopt(argv[1:], 'a:p:c:u:')

    @property
    def server_host(self):
        ip = self.__argv[1] if len(self.__argv) > 1 else DEFAULT_IP
        port = self.__argv[2] if len(self.__argv) > 2 else DEFAULT_PORT
        return ip, port

    @property
    def console_host(self):
        ip = DEFAULT_IP
        port = DEFAULT_PORT
        for opt, arg in self.__optlist:
            if opt == '-a':
                ip = arg
            elif opt == '-p':
                port = arg
        return ip, port

    @property
    def account_name(self):
        for opt, arg in self.__optlist:
            if opt == '-u':
                return arg
        return 'Anonymous'
