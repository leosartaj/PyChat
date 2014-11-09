try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readFile(fName):
    with open(fName) as f:
        lines = f.read()
    return lines

setup(
    name = 'PyGp',
    version = '0.0.0',
    author = 'Sartaj Singh',
    author_email = 'singhsartaj94@gmail.com',
    description = ('Asynchronous Chat Client'),
    long_description = readFile('README.md'),
    license = 'MIT',
    keywords = 'chat client server',
    url = 'http://github.com/leosartaj/PyGp',
    packages=['PyGp/client', 'PyGp/client/protocol'],
    scripts=['bin/client'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
