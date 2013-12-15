import requests, base64

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
	assert r.status_code == 200
	assert r.text.find('nisse') > 0
	assert r.text.find('petter') > 0

def test_content_length_protection():

	r = requests.post('%s/emptybody?eple=kake' % host)
	assert r.status_code == 200

	image_file = open("img/Centiped.png", "rb")
	base64_string = base64.b64encode(image_file.read())
	image_file.close()

	## Request fails due to error in urllib3 https://github.com/shazow/urllib3/issues/241
	## Implement with urllib2 directly?
	# r = requests.post('%s/smallbody' % host, data=base64_string)
	# assert r.status_code == 400

	r = requests.post('%s/largebody' % host, data=base64_string)
	assert r.status_code == 200
