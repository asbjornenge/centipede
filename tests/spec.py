import requests

host = 'http://127.0.0.1:8000'

def test_expose():
	r = requests.get('%s' % host)
	assert r.status_code == 200
	assert r.text == "HELO"

	r = requests.get('%s/params' % host)
	assert r.status_code == 200
	assert r.text.find('params') > 0