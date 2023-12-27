import socket
from threading import Thread

HOST = "localhost"
PORT = 10000
separator_token = "<SEP>"

try:
    client = socket.socket()
    print(f"Connecting to {HOST}:{PORT}...")

    client.connect((HOST, PORT))
    print("Connected.")
except:
    print("\nConnection could not be established.")
    exit(0)

try:
    nickname = input("Choose your nickname: ")
    print("Welcome to chat! Send 'q' to exit or press 'ctrl+C'.")
    client.send(f"{nickname} joined!".encode())
except:
    print("\nOoops, you lost connection!")
    exit(0)


def listen_for_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print("\n" + message)
        except:
            exit(0)


t = Thread(target=listen_for_messages)

t.daemon = True

t.start()


while True:
    try:
        to_send = input()
        if (to_send.lower() == 'q'):
            client.send(f"{nickname} left!".encode())
            break
        to_send = f"{nickname}{separator_token}{to_send}"

        client.send(to_send.encode())
    except KeyboardInterrupt:
        client.send(f"{nickname} left!".encode())
        break
    except:
        exit(0)

print("Ooops, you lost connection!")
client.close()