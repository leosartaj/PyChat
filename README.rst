PyChat
******

Installation
============
PyChat can be installed using pip
::

    pip install PyChat

Uninstalling
============
PyChat can be uninstalled using pip
::

    pip uninstall PyChat

Dependencies
============
PyChat is based on Python 2.7. PyChat uses Twisted and PyGTK.

Documentation
=============

Starting the application
------------------------
To start the application run the following command
::

    # Runs the application
    pychat [options]

* Run pychat -h/--help for various options.

In order to connect to a client, a server should be created. Server can be created inside the application or by starting a daemon server.

Starting a daemon server
------------------------
Clients connect to a server. Daemonized Server uses twisted's plugin system, twistd. To start a daemon server run the following commands.
::

    # Runs the daemon server
    twistd PyChat [options]

* Run twistd PyChat --help for various options

Bugs
====
.. |issues| replace:: https://github.com/leosartaj/PyChat/issues

For filing bugs raise an issue at |issues|
