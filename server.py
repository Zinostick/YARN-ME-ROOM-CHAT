import threading
import socket

host = "127.0.0.1"  #local host
port = 65014

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(6)
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handling_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} left the room '.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        print('server is listening...')
        client, address = server.accept()
        print(f'connection with {str(address)} is successful.')
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)


        print(f'nickname of the client is {nickname}')
        broadcast(f'{nickname} just joined the chat'.encode('utf-8'))
        client.send('çonnected to the server!'.encode('utf-8'))



        thread = threading.Thread(target=handling_client, args=(client,))
        thread.start()


print('server is listening...')
receive()
