import socket
import threading

host = '192.168.1.8'
port = 10000
LENGTH = 2000

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(LENGTH).decode('UTF-8')
            if message == 'Nickname':
                client.send(nickname.encode('UTF-8'))
                new_message = client.recv(LENGTH).decode('UTF-8')
                if new_message == 'Occupied':
                    print("This nickname is already occupied, reconnect with another one")
                    stop_thread = True
                else:
                    print(new_message)

            else:
                print(message)
        except:
            print("Ooops, you lost connection!")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('UTF-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()