# Description

A simple console chat with the ability to exchange 
messages over TCP/IP protocol on Python 3.10.

# Implementation

Imports of all required libraries are presented below


```python
from threading import Thread
import socket
import syslog
```

During implementation, communication between the client and
the server takes place via a TCP/IP socket. The socket is 
provided by the built-in library _**socket**_.

```python
host, port = '127.0.0.1', 7789

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
```

The socket.SOCK_STREAM parameter provides the ability 
to connect using the TCP protocol
The default port and host is localhost and host 7789, 
but others can be used.

The _receive_() function is used to receive new clients, 
transfer from the _handle_() function to the new thread, 
which in turn receives messages from clients and passes it 
to _broadcast_(), which sends messages to other clients

After receiving messages from clients, the server uses the 
Unix _**syslog**_ module to log messages.

```python
message = client.recv(1024)
syslog.syslog(syslog.LOG_INFO, message.decode('utf-8'))
```

The client side contains the _receive_() function for 
receiving messages from the server and, in case of receiving 
its own message, informs the client about the delivery.
The _write_() function is used to send messages from the client.

To simultaneously support a large number of clients, 
the _Thread_ function of the _**threading**_ module is 
used, which is responsible for creating a separate thread for each client.

```python
thread = Thread(target=handle, args=(client,))
thread.start()
```

Moreover, threads for each client are launched both 
on the server and on the client side.

```python
receive_thread = Thread(target=receive).start()
write_thread = Thread(target=write).start()
```

# Installation and launch

You can download distributions from GitHub:
https://www.github.com/rogaliiik/console_chat.git

Then, to start the server, move to the
project folder and open the distribution kit in the terminal window:

```
$ ./server
```

To connect the client, in a new terminal window,
open the distribution with:

```
$ ./client
```

(Note the default host is 127.0.0.1, port is 8080)

For all questions write to:
https://www.github.com/rogaliiik
