# README

A terminal based chat client. PyGp supports group chat feature only.

## Getting Started

Run the following commands to get a copy. 

```
# clone the repo
git clone https://github.com/leosartaj/PyGp.git

```

## Installation

Run the install script to install PyGp

```
# Installation script
./install.sh

```

## Uninstalling

Run the uninstall script to uninstall PyGp

```
# Uninstalls PyGp
./uninstall.sh

```

## Dependencies

PyGp is based on Python 2.7

## Documentation

### Starting a server
Clients connect to a server. To start a server run the following commands.

```
# Runs the server
pygp server [ip address] [options]

```

* Run pygp -h/--help for various options

The server maintains a log file in /usr/local/PyGp/PyGp\_server directory

### Starting a client
Clients connect to a server. To connect to a server run the following commands.

```
# Runs the client
pygp client [ip address of server] [options]

```

* Run pygp -h/--help for various options

### Additional Options

#### Sending a file

To send a file to other clients when connected to a server.

```

# Sends a file to other clients
# Type the following
file:[path of the file]

```

Note: Recieved files are kept in /usr/local/PyGp/PyGp\_recv directory
