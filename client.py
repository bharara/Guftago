from socket import *
from tkinter import *
from tkinter import filedialog
from threading import Thread
import os

def receive_msg():
    while True:
        try:
            msg = client_socket.recv(SIZE).decode("utf8")

            try:
                if msg[:9] == "/addnames":
                    namelist = msg.split("/")[2:]
                    for name in namelist:
                        user_list.insert(END, name)

                elif msg[:9] == "/addname/":
                    user_list.insert(END, msg[9:])
                elif msg[:8] == "/remove/":
                    print(msg)
                    user_list.delete (msg[8:])
                else:
                    msgs = msg.split('\n')
                    for msg in msgs:
                        msg_list.insert(END, msg)
            except:
                pass
        except:
            break


def send_msg (event=None):
    msg = textBox.get()
    textBox.set("")
    client_socket.send(bytes(msg, "utf8"))
    
    if msg == "/quit":
        Window.quit()


def closing (event=None):
    
    textBox.set("/quit")
    send_msg()

def select_file (event=None):
    filename = filedialog.askopenfilename(initialdir = "/",
        title = "Select file",
        filetypes = (("all files","*.*"), ("jpeg files","*.jpg")))


    client_socket.send(bytes('/file/' + filename, "utf-8"))

    fsize = os.path.getsize(filename)
    client_socket.send(str(fsize).encode('utf-8'))
    # ack = client_socket.recv(3).decode("utf8")
    # print (ack)

    f = open(filename, "rb")
    sendSize = 0

    while sendSize < fsize:
        sendS = min(fsize - sendSize, SIZE)
        l = f.read(sendS)
        client_socket.send(l)
        sendSize += len(l)
    f.close()


def downloadFile (event = None):

    filename = msg_list.get(msg_list.curselection()[0])

    index = filename.find(" Sent a file ")
    if index == -1: # NOT a file
        return 

    filename = filename[index + 13: ]

    serverDir = "files/"
    filename = serverDir + filename
    f = open(filename, "rb")
    data = f.read()

    f = filedialog.asksaveasfile(mode='wb')
    if f is None: return
    f.write(data)
    f.close()


# GUI
Window = Tk()
Window.title("guftaGo")

nowOnlinePart = Frame (Window)
onlineHeader = Label(nowOnlinePart, text="* Online").pack()
user_list = Listbox(nowOnlinePart, height = 30, width = 20)
user_list.pack()

nowOnlinePart.pack(side = RIGHT, fill = Y)
nowOnlinePart.pack()

leftPart = Frame(Window)

msgPart = Frame(leftPart)
scrollbar = Scrollbar(msgPart)
msg_list = Listbox(msgPart, height = 30, width = 100, yscrollcommand = scrollbar.set)
scrollbar.pack(side = RIGHT, fill = Y)
msg_list.pack(side = LEFT, fill = Y)
msg_list.bind('<<ListboxSelect>>', downloadFile)
msg_list.pack()
msgPart.pack()

textBox = StringVar()
textBox.set("...")
textBoxField = Entry(leftPart, textvariable = textBox)
textBoxField.bind("<Return>", send_msg)
textBoxField.pack()

send_button = Button(leftPart, text = "Send", command = send_msg).pack()
file_button = Button(leftPart, text = "Files", command = select_file).pack()

leftPart.pack(side = LEFT, fill = Y)
leftPart.pack()

Window.protocol("WM_DELETE_WINDOW", closing)


# Conecting
SIZE = 1024
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("10.7.53.55", 33002))

# Starting Recieve Thread
receiveThread = Thread(target=receive_msg).start()

# Starting GUI app
mainloop()