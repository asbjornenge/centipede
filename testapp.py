from centipede import expose, app

@expose('^/$')
def test(req):
	return "eple"

application = app()