from distutils import log
from setuptools import setup

try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        """
        Allows for clean uninstall
        Does not tamper with twisted
        """
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names

def readFile(fName):
    """
    Reads a given file
    """
    with open(fName) as f:
        lines = f.read()
    return lines

setup(
    name = 'PyChat',
    version = '1.2.1',
    author = 'Sartaj Singh',
    author_email = 'singhsartaj94@gmail.com',
    description = ('Asynchronous Chat Client'),
    long_description = readFile('README.md'),
    license = 'MIT',
    keywords = 'chat client server',
    url = 'http://github.com/leosartaj/PyChat',
    packages= ['PyChat', 'PyChat/client', 'PyChat/client/protocol', 'PyChat/client/gui', 'PyChat/client/gui/helper', 'twisted.plugins', 'PyChat/server', 'PyChat/server/protocol'],
    scripts=['bin/pychat'],
    package_data = {'PyChat/client/gui': ['*.glade']},
    install_requires = ['Twisted'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License',
        'Environment :: Plugins',
        'Framework :: Twisted',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ],
)

try:
    """
    Update Twisted Plugin Cache
    Normal user may not be able to do so
    """
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))
except Exception, e:
    log.warn("*** Failed to update Twisted plugin cache. ***")
    log.warn(str(e))
