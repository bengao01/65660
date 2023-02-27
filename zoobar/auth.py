from zoodb import *
from debug import *

import hashlib
import secrets

def newtoken(db, cred):
    hashinput = "%s.%s" % (secrets.token_bytes(16), cred.password)
    cred.token = hashlib.sha256(hashinput.encode('utf-8')).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    credDB = cred_setup()
    cred = credDB.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == password:
        return newtoken(credDB, cred)
    else:
        return None

def register(username, password):
    credDB = cred_setup()
    
    # Create new Cred Object
    cred = credDB.query(Cred).get(username)
    if cred:
        return None

    newCred = Cred()
    newCred.username = username
    newCred.password = password
    newCred.token = newtoken(credDB, newCred)
    credDB.add(newCred)
    credDB.commit()

    return newCred.token

def check_token(username, token):
    credDB = cred_setup()
    cred = credDB.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False
