import socket
import threading

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 45001))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == "NICKNAME":
                client.send(nickname.encode('ascii'))
            else:
                print(msg)
        except Exception as e:
            print(e)
            client.close()
            break


def write():
    while True:
        message = input("")
        msg = f'{nickname}: {message}'
        if message == "quit":
            client.close()
            break
        client.send(msg.encode("ascii"))


if __name__ == "__main__":
    receive_thr = threading.Thread(target=receive)
    receive_thr.start()
    write_thr = threading.Thread(target=write)
    write_thr.start()
