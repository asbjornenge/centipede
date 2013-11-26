from centipede import expose, app, params

@expose('^/$')
def _get(req):
	return "HELO"

@expose('^/params$')
@params()
def _params(req):
	return str(req.keys())

application = app()