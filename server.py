from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def addClients():
    
    while True:
        clientSocket, clientAddress = SERVER.accept()
        addresses[clientSocket] = clientAddress
        print(clientAddress, "joined.")

        clientSocket.send (bytes ("Welcome! Enter your name", "utf8"))
        Thread ( target = manage_client,
            args = (clientSocket,)).start()

def broadcast(msg, sender, prefix=""):

    for client in clients:
        client.send(bytes(prefix + msg, "utf8"))

## COMMAND FUNCTIONS

def close_client (clientSocket, name):
    clientSocket.send(bytes("/quit", "utf8"))
    clientSocket.close()
    del clients[clientSocket]
    broadcast(name + " has left the chat.", clientSocket)

def change_name (clientSocket, msg, oldName):
    newName = msg[6:]
    broadcast(oldName + " has changed it name to " + newName, clientSocket)
    return newName

    
# THE FUNCTION

def manage_client (clientSocket):
    
    name = clientSocket.recv(SIZE).decode("utf8")
    welcome = 'Hello ' + name + '!'
    clientSocket.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(msg, clientSocket)
    clients[clientSocket] = name

    while True:
        try:
            msg = clientSocket.recv(SIZE).decode("utf8")
        except:
            close_client (clientSocket, name)
            break

        if msg[0] != "/":
            broadcast(msg, clientSocket, name+": ")
        else: # Commands
            if msg == '/quit':
                close_client (clientSocket, name)
                break
            elif msg[:6] == '/name/':
                name = change_name (clientSocket, msg, name)


## MAIN IS APPROCHING
        
clients = {}
addresses = {}

PORT = 33001
SIZE = 1024

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('', PORT))


# THE MAIN
if __name__ == "__main__":

    SERVER.listen(5)
    print("Server is Ready...")

    addClientThread = Thread(target = addClients)
    addClientThread.start()
    addClientThread.join()
    
    SERVER.close()