try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'PyGp',
    version = '0.0.1',
    author = 'Sartaj Singh',
    author_email = 'singhsartaj94@gmail.com',
    description = ('Asynchronous Chat Client'),
    license = 'MIT',
    keywords = 'chat client server',
    url = 'http://github.com/leosartaj/PyGp',
    packages=[''],
    scripts=[''],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
