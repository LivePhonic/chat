import socket
import threading

host = '192.168.1.8'
port = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()
print(f'Ah shit, here we go again')

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def processing(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left!'.encode('ascii'))
            print(f'{nickname} disconnected')
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send('Nickname'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")
        client.send('Connected to server!'.encode('UTF-8'))
        broadcast(f"\n{nickname} joined!".encode('UTF-8'))

        thread = threading.Thread(target=processing, args=(client,))
        thread.start()

receive()