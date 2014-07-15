# README

A terminal based chat client. PyGp supports group chat only.

## Getting Started

Run the following commands to get a copy. 

```
# clone the repo
git clone https://github.com/leosartaj/jquery.ss.calculator.git

```
Note: Requires python 2.7 to run

## Documentation

### Starting a server
Clients connect to a server. To start a server run the following commands.

```
# change to the directory
cd [path/PyGp]
# Runs the server
python PyGp.py server [server name] [ip address]

```

The server maintains a log file in PyGp\_server directory

### Starting a client
Clients connect to a server. To connect to a server run the following commands.

```
# change to the directory
cd [path/PyGp]
# Runs the client
python PyGp.py client [name] [ip address of server]

```

### Additional Options

#### Sending a file

To send a file to other clients when connected to a server.

```
# Sends a file to other clients
# Type the following
file:[path of the file]

```

Note: Recieved files are kept in PyGp\_recv directory
