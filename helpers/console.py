import getopt
from config.params import *


def host_params(argv, strict=False):
    if not strict:
        return argv[1] if len(argv) > 1 else DEFAULT_IP, argv[2] if len(argv) > 2 else DEFAULT_PORT
    optlist, args = getopt.getopt(argv[1:], 'a:p:w')
    ip = DEFAULT_IP
    port = DEFAULT_PORT
    for opt, arg in optlist:
        if opt == '-a':
            ip = arg
        elif opt == '-p':
            port = arg
    return ip, port
