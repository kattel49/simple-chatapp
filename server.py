import socket
import threading

host = "127.0.0.1"
port = 45001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(server)

clients = []
nicknames = []

# send message to all clients
def broadcast(msg):
    for client in clients:
        client.send(msg)

# handle client connections
def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            # index of the client 
            index = clients.index(client)
            # remove the client from clients
            clients.remove(client)
            client.close()
            # remove the attached nickname
            nicknames.remove(nicknames[index])
            broadcast(f'{nicknames[index]} left the chat'.encode('ascii'))
            break


def receive():
    while True:
        print("Waiting for connection")
        client, address = server.accept()
        print(f"Connected to {client} at {str(address)}")

        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the {client} is {nickname}")

        broadcast(f"{nickname} joined the chat".encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    print("The server is running")
    receive()