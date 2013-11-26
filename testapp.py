from centipede import expose, app

@expose('^/$')
def test(req):
	return "HELO"

application = app()