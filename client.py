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

a = None
while True:
  print("1. Registering with RS")
  print("2. Requesting the Peer List")
  print("3. Leave the network")
  a = int(input("Enter your request: "))
  if a == 1:
    s1 = socket.socket()
    s1.connect((Host_RS,Port_RS))
    x = 'Register_to_RS'
    message = x + ' <cr> <lf>\nHostname ' + hostname + ' <cr> <lf>\nPortnumber ' + str(portnumber) + ' <cr> <lf>\n'
    s1.send(message.encode())
    received_message = s1.recv(2048).decode()
    print(received_message)

