# README

PyChat is an asynchronous chat client.

## Installation

PyChat can be installed using pip

```
pip install PyChat

```

## Uninstalling

PyChat can be uninstalled using pip

```
pip uninstall PyChat

```

## Dependencies

PyChat is based on Python 2.7. PyChat uses Twisted Framework.

## Documentation

### Starting a server
Clients connect to a server. Server uses twisted's plugin system, twistd. To start a server run the following commands.

```
# Runs the server
twistd PyChat [options]

```

* Run twistd PyChat --help for various options

### Starting a client
Clients connect to a server. To connect to a server run the following commands.

```
# Runs the client
pychat [interface] [options]

```

* Run pychat -h/--help for various options
