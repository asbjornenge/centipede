import json
from centipede import expose, app, query_string, body_data, map

## Basic
#

@expose('^/$')
def _get(req):
	return "HELO"

## Decorators
#

@expose('^/basicmap$')
@map('QUERY_STRING','test')
def _basicmap(req):
	return json.dumps(req['test'])

@expose('^/params$')
@query_string()
def _params(req):
	return json.dumps(req['query'])

@expose('^/bodydata$', method='POST')
@query_string()
@body_data()
def _bodydata(req):
	data = {
		'body'  : req['body'],
		'query' : req['query']
	}
	return json.dumps(data)

## Bunch
#

from bunch import Bunch

def butcher(data):
	return Bunch(data)

@expose('^/butch$', method='POST')
@body_data()
@map('body','butched', parser=butcher)
def _butch(req):
	return json.dumps(req['butched'])

application = app()