import socket
import threading

host = '192.168.1.8'
port = 10000

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('UTF-8')
            if message == 'Nickname':
                client.send(nickname.encode('UTF-8'))
            else:
                print(message)
        except:
            print("Ooops, you lost connection!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('UTF-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()