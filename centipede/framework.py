##
#                  ,           /)   
#   _   _ __  _/_   __    _  _(/  _ 
#  (___(/_/ (_(___(_/_)__(/_(_(__(/_
#                .-/                
#               (_/     
#
#  http://code.google.com/p/centipede/
#  Understanding & simplicity
#  Copyright 2010, Asbjorn Enge. All rights reserved.
#
#  LICENSE.txt
#
##
#
#  The expose decorator is inspired by the bespin project.
#  http://mozillalabs.com/bespin/
#
##
#
#  Framework
#
##

from webob import Request, Response
from urlrelay import url, URLRelay
from static import Cling
from urllib import unquote, unquote_plus

status_map = {
    200: "200 OK",
    301: "301 Moved Permanently",
    302: "302 Found",
    303: "303 See Other",
    304: "304 Not Modified",
    307: "307 Temporary Redirect",
    400: "400 Bad Request",
    401: "401 Unauthorized",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    418: "418 I'm a teapot",
    500: "500 Internal Server Error",
    502: "502 Bad Gateway",
    503: "503 Service Unavailable",
    504: "504 Gateway Timeout"
}

## Expose urls
#

def expose(url_pattern, method='GET', content_type='text/html', charset='UTF-8'):
    """ Expose this function to the world, matching the given URL pattern and, optionally, HTTP method, ContentType and Charset.
    """
    def entangle(func):
        @url(url_pattern, method)
        def wrapped(env, start_response):
            status  = 200
            headers = [('Content-type', '%s; charset=%s' % (content_type, charset))]
            params(env, method)
            resp    = func(env)

            if type(resp) == tuple:
                status  = resp[0]
                heads   = resp[2]
                resp    = resp[1]
                for h in heads.keys():
                    headers.append((h,heads[h]))

            start_response(status_map[status], headers)
            return [resp]
    return entangle

## Grab the params
#

param_keys = {
    'query_string' : {
        'wsgi_env_key'   : 'QUERY_STRING',
        'need_read'      : False,
        'centipede_key'  : 'params',
        'unquote_method' : unquote
    },
    'form_data' : {
        'wsgi_env_key'   : 'wsgi.input',
        'need_read'      : True,
        'centipede_key'  : 'data',
        'unquote_method' : unquote_plus
    }
}

def params(env, method):

    for param in param_keys.values():
        env[param['centipede_key']] = {}
        env['%s_raw' % param['centipede_key']] = {}
        try:
            data = env[param['wsgi_env_key']]
            if param['need_read']:
                data = data.read()
            if data != None and data != '':
                for keyval in data.split('&'):
                    k,v = keyval.split('=')
                    uq  = param['unquote_method']
                    env[param['centipede_key']][uq(k)] = uq(v)
                    env['%s_raw' % param['centipede_key']][k] = v
        except:
            print "Unable to parse %s data." % param['wsig_env_key']


## Make the application
#

def app(static=None):
    """ Return wsgi app
    """
    if static != None:
        static = Cling(static)
        app = URLRelay(default=static)
    else:
        app = URLRelay()
    return app

