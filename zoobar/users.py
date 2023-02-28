from flask import g, render_template, request, Markup

from login import requirelogin
from zoodb import *
from debug import *
# import bank

import rpclib
sys.path.append(os.getcwd())
import readconf

@catch_err
@requirelogin
def users():
    args = {}
    args['req_user'] = Markup(request.args.get('user', ''))
    if 'user' in request.values:
        persondb = person_setup()
        user = persondb.query(Person).get(request.values['user'])
        if user: 
            p = user.profile
            if p.startswith("#!python"):
                import profile
                p = profile.run_profile(user)

            p_markup = Markup("<b>%s</b>" % p)
            args['profile'] = p_markup

            args['user'] = user

            host = readconf.read_conf().lookup_host('bank')
            with rpclib.client_connect(host) as c:
                args['user_zoobars'] = c.call('balance', username=user.username)
            with rpclib.client_connect(host) as c:
                args['transfers'] = c.call('get_log', username=user.username)
            # args['user_zoobars'] = bank.balance(user.username)
            # args['transfers'] = bank.get_log(user.username)
        else:
            args['warning'] = "Cannot find that user."
    return render_template('users.html', **args)
