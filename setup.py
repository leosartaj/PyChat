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
    name = 'PyGp',
    version = '1.0.0',
    author = 'Sartaj Singh',
    author_email = 'singhsartaj94@gmail.com',
    description = ('Asynchronous Chat Client'),
    long_description = readFile('README.md'),
    license = 'MIT',
    keywords = 'chat client server',
    url = 'http://github.com/leosartaj/PyGp',
    packages= ['PyGp', 'PyGp/client', 'PyGp/client/protocol', 'PyGp/client/gui', 'twisted.plugins', 'PyGp/server', 'PyGp/server/protocol'],
    scripts=['bin/pygpcli'],
    install_requires = ['Twisted'],
    package_data = {'PyGp/client/gui': ['*.glade']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
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
