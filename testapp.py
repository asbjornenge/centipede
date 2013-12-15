import json
from centipede import expose, app, query_string, body_data, map

@expose('^/$')
def _get(req):
	return "HELO"

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

application = app()