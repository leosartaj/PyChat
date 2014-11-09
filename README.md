# README

A simple chat client.

## Installation

PyGp can be installed using pip

```
pip install PyGp

```

## Uninstalling

PyGp can be uninstalled using pip

```
pip uninstall PyGp

```

## Dependencies

PyGp is based on Python 2.7. PyGP uses Twisted Framework.

## Documentation

### Starting a server
Clients connect to a server. Server uses twisted's plugin system, twistd. To start a server run the following commands.

```
# Runs the server
twistd PyGp [options]

```

* Run twistd PyGp --help for various options

### Starting a client
Clients connect to a server. To connect to a server run the following commands.

```
# Runs the client
pygpcli [options]

```

* Run pygpcli -h/--help for various options
