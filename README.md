# Introduction:

We creating a chatting app called guftaGo. It is a multi-user chat room that allows user to connect on a local LAN. User can see who is online, share messages and files etc.

## Features:

- See who is online
- Send messages to the group
- Send files to be stored on the server
- Download files that others have uploaded using GUI
- Mute the chat for some time
- Quit the chat using in-chat commands
- Change your name
- See in-chat commands for help

## Tools used:

- Python Socket for Networking
- Python Tkinter for GUI

## Problems Encountered:

- Our main problem was establishing a protocol between client and server that can send instructions not be displayed in the chat.
  - We solved it by agreeing on the syntax of **&quot;/command/argument/&quot;**. If user send something in this syntax that is not a valid command, the user is politely informed that it is invalid.
- We encountered problem when sending a file to server.
  - We solved this by sending the file size beforehand and then waiting for the file data for that many bytes
