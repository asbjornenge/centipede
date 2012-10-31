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
#  Controllers
#
##

from centipede import expose, app

@expose('^/$')
def index(request):
    """ Simple Hello IgglePigglePartyPants
    """
    return 'Hello IgglePigglePartyPants!'

@expose('^/google$')
def index(request):
    """ A redirect
    """
    return (307, '', {'Location':'http://google.com'})
 
import json
 
@expose('^/params$', 'GET', content_type='application/json')
def twitter(request):
    """ JSON dump the params
    """
    return json.dumps(request['params'])
    
application = app()


