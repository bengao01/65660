from zoodb import *
from debug import *

import time

import rpclib
sys.path.append(os.getcwd())
import readconf

def transfer(sender, recipient, zoobars, token):
    # Verify supplied token
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        isValid = c.call('check_token', username=sender, token=token)
        if not isValid:
            return

    bankDB = bank_setup()
    senderp = bankDB.query(Bank).get(sender)
    recipientp = bankDB.query(Bank).get(recipient)

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankDB.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def profile_transfer(sender, recipient, zoobars, service):
    log(service)

    # if (service != "profile") {
    #     raise ValueError
    # }

    bankDB = bank_setup()
    senderp = bankDB.query(Bank).get(sender)
    recipientp = bankDB.query(Bank).get(recipient)

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankDB.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    db = bank_setup()
    bank = db.query(Bank).get(username)
    return bank.zoobars

def create(username):
    db = bank_setup()
    bank = db.query(Bank).get(username)
    if bank is not None:
        return bank.zoobars
    newBank = Bank()
    newBank.username = username
    newBank.zoobars = 10
    db.add(newBank)
    db.commit()
    return newBank.zoobars

def get_log(username):
    db = transfer_setup()
    l = db.query(Transfer).filter(or_(Transfer.sender==username,
                                      Transfer.recipient==username))
    r = []
    for t in l:
       r.append({'time': t.time,
                 'sender': t.sender ,
                 'recipient': t.recipient,
                 'amount': t.amount })
    return r 


