# Import socket module 
import socket		
import os
import datetime	 

#List_of_RFCs = C:\Internet_Protocols\List_of_RFCs
#csv_receivedlist = C:\Internet_Protocols\Received_list

Port_RS = 23471
Host_RS = '192.168.0.148'

hostname = socket.gethostbyname(socket.gethostname())
print(hostname)
portnumber = 10000

# Create a socket object
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		  
#s.connect((Host_RS,Port_RS )) 

def registration():
    x = 'Register_to_RS'
    message = x + ' <cr> <lf>\nHostname ' + hostname + ' <cr> <lf>\nPortnumber ' + str(portnumber) + ' <cr> <lf>\n'
    s.send(message.encode())
    received_message = s1.recv(2048).decode()
    print(received_message)
    s.close()

def requesting_peerlist():
    


    
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
      

