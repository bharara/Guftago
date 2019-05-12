from socket import *
from threading import Thread
from time import sleep


def send_to_all(msg, sender):

    for socket in sockets:
        socket.send(bytes(msg, "utf8"))

## COMMAND FUNCTIONS

def close_client (clientSocket, name):
    clientSocket.send(bytes("/quit", "utf8"))
    clientSocket.close()
    del sockets[clientSocket]
    send_to_all(name + " has left the chat.", clientSocket)
    send_to_all("/remove/"+name, clientSocket)


def change_name (clientSocket, msg, oldName):
    newName = msg[6:]
    send_to_all(oldName + " has changed it name to " + newName, clientSocket)

    send_to_all("/remove/"+oldName, clientSocket)
    send_to_all("/addname/"+newName, clientSocket)

    return newName

def recieveFile (clientSocket, msg, name):
    
    filename = msg.split ('/')[-1]
    msg = name + " Sent a file " + filename
    filename = "files/" + filename

    f = open(filename, 'wb')

    fileSize = int(clientSocket.recv(SIZE).decode('utf-8'))

    sentSize = 0
    while sentSize < fileSize:
        getS = min(fileSize - sentSize, SIZE)
        data = clientSocket.recv(getS)
        sentSize += len(data)
        f.write(data)
    f.close()

    send_to_all(msg, clientSocket)
    
def welcome (clientSocket):

    name = clientSocket.recv(SIZE).decode("utf8")

    # Informing the herd
    msg = 'Hello ' + name + '! Welcome to the Chat \nType /help to learn Commands'
    clientSocket.send(bytes(msg, "utf8"))
    send_to_all(name + " is Here!", clientSocket)

    ## Online List
    send_to_all("/addname/"+name, clientSocket)
    msg = '/addnames'
    for names in sockets.values():
        msg = msg +"/" + names
    clientSocket.send(bytes(msg, "utf8"))


    sockets[clientSocket] = name

    return name





# THE FUNCTION

def addClients():
    
    while True:
        clientSocket, clientAddress = SERVER.accept()
        print(clientAddress, "joined.")

        clientSocket.send (bytes ("Welcome! Enter your name", "utf8"))
        Thread ( target = manage_client,
            args = (clientSocket,)).start()

def manage_client (clientSocket):
    
    name = welcome (clientSocket)

    while True:
        try:
            msg = clientSocket.recv(SIZE).decode("utf8")
        except:
            close_client (clientSocket, name)
            break

        if msg[0] != "/":
            send_to_all(name + ": " + msg, clientSocket)
        else: # Commands
            if msg == '/quit':
                close_client (clientSocket, name)
                break
            elif msg[:6] == '/name/':
                name = change_name (clientSocket, msg, name)
            elif msg[:6] == '/file/':
                uploadThread = Thread ( target = recieveFile,
                    args = (clientSocket, msg, name, ))
                uploadThread.start()
                uploadThread.join()
            elif msg[:7] == '/sleep/':
                msg = msg[7:]
                try:
                    delay = int(msg)
                    sleep (delay)
                except:
                    clientSocket.send(bytes('INVALID COMMAND', "utf8"))
            elif msg == "/help":
                msg = """/quit - to Exit \n/name/<name> - to rename yourself \n/file/<filename> - to send file \nClick on file link to download file \n/sleep/<time> - to mute thread \n/help - to get help \n"""
                clientSocket.send(bytes(msg, "utf8"))
            else:
                clientSocket.send(bytes('INVALID COMMAND', "utf8"))


## MAIN IS APPROCHING
        
sockets = {}

SIZE = 1024
MAX_CONN = 8

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('', 33002))


SERVER.listen(MAX_CONN)
print("Server is Ready...")

addClientThread = Thread(target = addClients)
addClientThread.start()
addClientThread.join()

SERVER.close()