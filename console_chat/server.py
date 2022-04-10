"""
The module responsible for the operation
of the server side of the console chat
"""

from threading import Thread
import socket
import syslog


def server_info():
    """Gets host and port information"""
    host = input("Choose host in format '127.0.0.1', 'Enter' for 'localhost': ")
    port = input("Choose port in format '1111', 'Enter' for '8080': ")
    if host == '':
        host = '127.0.0.1'
    if port == '':
        port = 8080
    else:
        port = int(port)
    return host, port


def broadcast(message):
    """Sends message to all active users"""
    for client in clients:
        client.send(message)


def handle(client):
    """Receives a message from the client, logs it and broadcast"""
    while True:
        try:
            message = client.recv(1024)
            syslog.syslog(syslog.LOG_INFO, message.decode('utf-8'))
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive(server):
    """Accepts users, collects information and passes it to handle()"""
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('ENTER NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"New client's nickname: {nickname}!")
        broadcast(f'New client {nickname} joined the chat! '.encode('utf-8'))
        client.send('You were connected to the server!'.encode('utf-8'))

        thread = Thread(target=handle, args=(client,)).start()


if __name__ == '__main__':
    host, port = server_info()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []
    nicknames = []

    print('Waiting for clients...')
    receive(server)
