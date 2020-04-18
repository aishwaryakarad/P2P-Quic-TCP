# Import socket module 
import socket		
import os
import datetime	 
import json

List_of_RFCs = 'C:\Internet_Protocols\List_of_RFCs'
#csv_receivedlist = 'C:\Internet_Protocols\Received_list'
peer_list = []

Port_RS = 23472
Host_RS = '192.168.0.148'

hostname = socket.gethostname()
print(hostname)
portnumber = 10000

# Create a socket object
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		  
#s.connect((Host_RS,Port_RS )) 

def registration():
    x = 'Register_to_RS'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    recv_msg = json.loads(received_message)
    print(recv_msg["msg"])
    s.close()

def requesting_peerlist():
    x = 'Active_peer'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    print(received_message)
    recv_msg = received_message[received_message.index('\n')+4:]
    s.close()

def leave_message():
    x = 'Leave_the_server'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    #recv_msg = json.loads(received_message)
    print(received_message)
    s.close()
       
def peer_list_files():
    global exisiting_files
    for root, dirs, files in os.walk(List_of_RFCs):
        #print(files)
        for file in files:
            if '.txt' in file:
                peer_list.append(file.split(".")[0])

peer_list_files()


choice = None
while True:
    print("1. Registering with RS\n 2. Requesting the Active Peer List\n 3. Leave the network")
    choice = int(input("Enter your request: "))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host_RS,Port_RS))
    if choice == 1:
        registration()
    elif choice == 2:
        requesting_peerlist()
    else:
        leave_message()