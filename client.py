from socket import *
from tkinter import *
from threading import Thread

def receive_msg():
    while True:
        try:
            msg = client_socket.recv(SIZE).decode("utf8")
            msg_list.insert(END, msg)
        except:
            break


def send_msg (event=None):
    msg = textBox.get()
    textBox.set("")
    client_socket.send(bytes(msg, "utf8"))
    
    if msg == "/quit":
        #client_socket.close()
        Window.quit()


def closing (event=None):
    
    textBox.set("/quit")
    send_msg()


# GUI
Window = Tk()
Window.title("gupShup")

msgPart = Frame(Window)
scrollbar = Scrollbar(msgPart)
msg_list = Listbox(msgPart, height = 30, width = 100, yscrollcommand = scrollbar.set)
scrollbar.pack(side = RIGHT, fill = Y)
msg_list.pack(side = LEFT, fill = BOTH)
msg_list.pack()
msgPart.pack()


textBox = StringVar()
textBox.set("...")
textBoxField = Entry(Window, textvariable = textBox)
textBoxField.bind("<Return>", send_msg)
textBoxField.pack()

send_button = Button(Window, text = "Send", command = send_msg)
send_button.pack()

Window.protocol("WM_DELETE_WINDOW", closing)


# MAIN
HOST = "10.7.53.55"
PORT = 33001
SIZE = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))

receiveThread = Thread(target=receive_msg)
receiveThread.start()
mainloop()