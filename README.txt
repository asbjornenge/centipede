===============
Centipede 0.2.5
===============

Centipede is a WSGI microframework with a simple decorator based router. It's strength is that it models the technology in use and tries not to confuse developers with complex patterns and tricks. It inherits strongly from urlrelay_.

Installation
============
::

    $ pip install centipede

Defining handlers
=================
With Centipede you expose functions to urls. Functions either return a **string** or a **tuple**. A string is treated as the document body, http status is set to *200 OK* and returned to the browser. Should you return a tuple, *status code*, *body* and *headers* are expected. The expose decorator also supports a few arguments.

::

    from centipede import expose, app

    @expose('^/$')
    def index(request):
        """ Simple Hello
        """
        return 'Hello IgglePigglePartyPants!'

    @expose('^/google$')
    def index(request):
        """ A redirect
        """
        return (307, '', {'Location':'http://google.com'})
 
    import json
    
    @expose('^/twitter','POST',content_type='application/json')
    def tweet_post(request):
        """ Tweet
        """
        data  = request['data']
        text  = data['text']
        user  = data['user']
        tweet = magic.tweet(text, user)
        return json.dumps(tweet)
 
    @expose('^/twitter/(?P<tweet>\w+)$','GET',content_type='application/json')
    def twitter(request):
        """ Get a tweet
        """
        id    = req['wsgiorg.routing_args'][1]['tweet']
        meta  = request['params']['metadata']
        tweet = magic.get_tweet(id, meta=meta)
        return json.dumps(tweet)
    
    application = app()


Expose arguments
================
The expose decorator looks like this::

    expose(url_pattern, method='GET', content_type='text/html', charset='UTF-8')

Request
=======
The parameter passed to the functions exposed (*request* in the examples above) is the WSGI environ_ dictionary. For convenience the **query string parameters** and **form data** parameters are packed into environ's **params** and **data** keys.

Query string data
-----------------
For convenience, query string parameters are available as a dictionary in environ's **params** key. Both key and value are unquoted using *urllib.unquote*. Unquoted parameters are passed to the **params_raw** key.


Form data
---------
For convenience, form data are available as a dictionary in environ's **data** key. Both key and value are unquoted using *urllib.unquote_plus*. Unquoted parameters are passed to the **data_raw** key.


Templates
=========
I would recommend keeping your html templates static on the client side and use a javascript template library. But if you really need some server side templating, have a look at mako.

Static files
============
For production you should always host your static files directly from the webserver or a varnish cache or something. But for development purposes you can have centipede serve your static files by passing *app* a parameter::

	app('path/to/static')

Deployment
==========
For deployment it is a good idea to run your centipede application behind a good WSGI server. There is a bunch_. Gunicorn_ is good. I usually end up running uwsgi_ behind nginx.

Changelog
=========

0.2.5
-----
* Separated query string params and form data
* Form data in *data* key
* Query string params in *params* key
* Improved error handling for unpacking params (needs more work)

0.2.4
-----
* Added urllib.unquote_plus for POST parameters.
* Added *params_raw* key to environ in case urllib.unquote mess up your parameters.

0.2.3
-----
* Added *params* key to environ for easy parameter access.
* Added urllib.unquote for params

enjoy.

.. _urlrelay: http://pypi.python.org/pypi/urlrelay/
.. _environ: http://www.python.org/dev/peps/pep-0333/#environ-variables
.. _Gunicorn: http://gunicorn.org/
.. _uwsgi: http://projects.unbit.it/uwsgi/
.. _bunch: http://www.wsgi.org/en/latest/servers.html
