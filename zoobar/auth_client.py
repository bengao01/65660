from debug import *
from zoodb import *
import rpclib

sys.path.append(os.getcwd())
import readconf
import auth

def login(username, password):
    # return auth.login(username, password)
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        ret = c.call('login', username=username, password=password)
        return ret


def register(username, password):
    # return auth.register(username, password)
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        ret = c.call('register', username=username, password=password)
        return ret


def check_token(username, token):
    # return auth.check_token(username, token)
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        ret = c.call('check_token', username=username, token=token)
        return ret

