from distutils.core import setup

setup(
    name='centipede',
    version='0.2.5',
    license='FreeBSD',
    packages=['centipede',],
    author='Asbjorn Enge',
    author_email='asbjorn@asbjornenge.com',
    url='http://centipede.asbjornenge.com',
    description='Centipede is a WSGI microframework with a simple decorator based router.',
    long_description=open('README.txt').read(),
    install_requires=[
        "WebOb==1.2b2",
        "urlrelay==0.7.1",
        "wsgiref==0.1.2",
        "static==0.4"
    ],
)
