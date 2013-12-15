import requests

host = 'http://127.0.0.1:8000'

def test_basics():
	r = requests.get('%s' % host)
	assert r.status_code == 200
	assert r.text == "HELO"

def test_decorators():
	r = requests.get('%s/basicmap?eple=kake' % host)
	assert r.status_code == 200
	assert r.text.find('eple') > 0

	r = requests.get('%s/params?eple=kake' % host)
	assert r.status_code == 200
	assert r.text.find('eple') > 0

	r = requests.post('%s/bodydata?eple=kake' % host, data={'nisse':'petter'})
	assert r.status_code == 200
	assert r.text.find('eple') > 0
	assert r.text.find('kake') > 0
	assert r.text.find('nisse') > 0
	assert r.text.find('petter') > 0

def test_butch_wrapper():
	r = requests.post('%s/butch' % host, data={'nisse':'petter'})
	print r.status_code
	assert r.status_code == 200
	assert r.text.find('nisse') > 0
	assert r.text.find('petter') > 0

	# TODO: Test combination og query_string and body_data
