#!/usr/bin/env python3

import rpcsrv
import sys
import bank
from debug import *

class BankRpcServer(rpcsrv.RpcServer):
    def rpc_create(self, username):
        return bank.create(username)
    def rpc_balance(self, username):
        return bank.balance(username)
    def rpc_transfer(self, sender, recipient, zoobars):
        return bank.transfer(sender, recipient, zoobars)
    def rpc_get_log(self, username):
        return bank.get_log(username)

if len(sys.argv) != 2:
    print(sys.argv[0], "too few args")

s = BankRpcServer()
s.run_fork(sys.argv[1])
