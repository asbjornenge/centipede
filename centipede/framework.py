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

import traceback

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
            # params(env, method)
            resp    = func(env)

            if type(resp) == int:
                status = resp
                resp   = status_map.has_key(status) and status_map[status] or ''
            elif type(resp) == tuple:
                if len(resp) > 2:
                    heads = resp[2]
                    for h in heads.keys():
                        headers.append((h,heads[h]))
                if len(resp) < 2:
                    status = 500
                    resp   = 'CENTIPEDE ERROR: Returning a tuple requires minimum two values'
                else:
                    status = resp[0]
                    resp   = resp[1]
            elif type(resp) not in [str,unicode]:
                status = 500
                resp   = 'CENTIPEDE ERROR: Unsupported return value %s. Use str, unicode, int or tuple.' % type(resp)
                
            start_response(status_map.has_key(status) and status_map[status] or '%s' % status, headers)
            return [resp]
    return entangle

## Helpers
#

def reflect(req):
    return req

def parse_params(data, unquote_method=reflect):
    d = {}
    if len(data) == 0:
        return d
    for keyval in data.split('&'):
        k,v = keyval.split('=')
        d[unquote_method(k)] = unquote_method(v)
    return d

## Decorators
#

def map(wsgi_key, centipede_key, wrap_request=reflect, parse_params=reflect):
    def func_wrapper(func):
        def request_wrapper(req):
            req[centipede_key] = parse_params(req[wsgi_key])
            return func(wrap_request(req))
        return request_wrapper
    return func_wrapper

def query_string(key='query', wrapper=reflect, unquote_method=unquote, param_parser=None):
    if unquote_method == None:
        unquote_method = reflect
    def parse(data):
        return parse_params(data, unquote_method=unquote_method)
    param_parser = param_parser != None and param_parser or parse
    return map('QUERY_STRING', key, wrap_request=wrapper, parse_params=param_parser)

def body_data(key='data', wrapper=reflect, unquote_method=unquote_plus, param_parser=None, max_size=100000):
    if unquote_method == None:
        unquote_method = reflect
    # TODO : Return error if data > max_size
    def parse(data):
        return parse_params(data.read(), unquote_method=unquote_method)
    param_parser = param_parser != None and param_parser or parse
    return map('wsgi.input', key, wrap_request=wrapper, parse_params=param_parser)


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

