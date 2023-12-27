import socket
from threading import Thread


HOST = ''
PORT = 10000
separator_token = "<SEP>"

clients = set()

server = socket.socket()

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen(5)
print("Ah shit, here we go again")


def send_to_chat(message):
    for client in clients:
        client.send(message.encode())


def listen_for_client(cs):
    while True:
        try:
            message = cs.recv(1024).decode()
            if not message:
                print(f"{address} disconnected.")
                clients.remove(cs)
                break
        except:
            print(f"{address} disconnected.")
            clients.remove(cs)
            break
        else:
            message = message.replace(separator_token, ": ")
        send_to_chat(message)


while True:
    client, address = server.accept()
    print(f"{address} connected.")

    clients.add(client)

    t = Thread(target=listen_for_client, args=(client,))

    t.daemon = True

    t.start()
