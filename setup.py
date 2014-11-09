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
    packages= ['PyGp', 'PyGp/client', 'PyGp/client/protocol', 'PyGp/client/gui'],
    scripts=['bin/client'],
    package_data = {'PyGp/client/gui': ['*.glade']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
