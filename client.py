import socket		
import os
#import datetime	 
import json
import traceback, sys 
import csv
#import pandas as pd

List_of_RFCs = 'C:\\Internet_Protocols\\List_of_RFCs'
csv_receivedlist = 'C:\\Internet_Protocols\\Received_list\\csv_receivedlist.csv'
peer_list = []

Port_RS = 23473
Host_RS = '192.168.0.161'

hostname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip1 = (s.getsockname()[0])
print(hostname)
portnumber = 10000

# Create a socket object
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		  
#s.connect((Host_RS,Port_RS ))

class peerserver():
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

def registration():
    x = 'Register_to_RS'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    print(received_message)
    recv_msg = json.loads(received_message)
    print(recv_msg["msg"])
    s.close()

def check_rfc(request):
    r = []
    for rfcs in request.split(","):
            if rfcs not in peer_list:
                rfcs = rfcs.strip()
                r.append(rfcs)
                #print(r)
    return r

def requesting_peerlist():
    rfc_request = input("Enter the rfc to be requested: ")
    rfc = check_rfc(rfc_request)
    #print(rfc)
    x = 'Active_peer'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    print(received_message)
    recv_message = received_message.split('\n')
    #print(type(recv_message), len(recv_message), recv_message)
    if len(recv_message) == 1:
        print("No peers active")
        s.close()
    else:
        new_msg = recv_message[1]
        #print(type(new_msg))
        new_msg = new_msg.strip('[').strip(']').replace('}, {', '}!{').split('!')
        res = []
        for item in new_msg:
            res.append(json.loads(item))
        print(res)
        for element in res:
            peer = peerserver(**element)
            print(peer)
            try:
                if(requesting_rfcs(peer, rfc)):
                    break
            except Exception:
                traceback.print_exc(sys.stdout)
        if(len(res) != 0):
            print("No active peer left to check")
    s.close()
    
def checking_list(msg):
    f = open(csv_receivedlist)
    csv_f = csv.reader(f)
    list1 = []
    attendee_emails = []
    for row in csv_f:

        d = row[0].split(";")
        attendee_emails.append(d)
    #print('abc',attendee_emails)
    #print('msg',msg)
    for i in msg:
        #b = i[0]
        c = i[0].split(";")

        if c in attendee_emails:
            pass
        else:
            count = 0
            for j in attendee_emails:
                if c[0] == j[0] and c[1] == j[1] and c[2] == j[2]:
                    #print("in loop")
                    ind = attendee_emails.index(j)
                    attendee_emails[ind] = c
                    count +=1
                    
            if count == 0:
                attendee_emails.append(c)
                list1.append(c)
   # print(list1)
    return list1


def requesting_rfcs(peer: peerserver, rfc):
    print(rfc)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(peer.port)
    ip = peer.ip
    s1.connect((ip, port))
    x = 'listofrfcs'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s1.send(message.encode())
    received_message = s1.recv(2048).decode()
    #print(received_message)
    recv_message = received_message.split('\n')
    #print(type(recv_message), len(recv_message), recv_message)
    new_msg = recv_message[2]
    #print(new_msg) 
    r_msg = json.loads(new_msg)
    print(r_msg)
    res_msg = checking_list(r_msg)
    print("-------------------------------------------")
    print(res_msg)
    print("-------------------------------------------")
    for IPList in res_msg:
        #print("Here")
        #IPList = item[0].split(',')
        #print(IPList)
        texttype = IPList[0].split('.')[0]
        ip_1 = IPList[1]
        port_1 = IPList[2]
        flag = IPList[3]
        reg_rfc_in_csv(texttype, ip_1, port_1, flag)
        
    if new_msg == '[]':
        res = 0
    else:
        print("Im here")
        res = json.loads(new_msg)
        #print(res)
        for element in res:
            IPList = element[0].split(';')
            texttype = IPList[0].split('.')[0]
            ip_1 = IPList[1]
            port_1 = IPList[2]
            print(texttype)
            for i in rfc:
                if texttype == i:
                    #print(ip_1)
                    #print(port_1)
                    try:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s2.connect((ip_1,int(port_1)))
                        x = 'Requesting_files'
                        message = json.dumps({"msg" : x ,"file" : i, "Hostname" : hostname , "Portnumber" : str(portnumber)})
                        print(message)
                        s2.send(message.encode())
                        flag = '1'
                        reg_rfc_in_csv(i, ip1, portnumber, flag)
                        print("Im")
                        recv_rfc_file(i, s2)
                    except Exception:
                        traceback.print_exc(sys.stdout)
                    finally:
                        s2.close
    s1.close()
    return False

def recv_rfc_file(rfc, s):
    completeName = os.path.join(List_of_RFCs, str(rfc) + ".txt")
    with open(completeName, 'wb') as file:
        while True:
            data = s.recv(2048)
            if not data:
                break
            file.write(data)
    file.close()

def reg_rfc_in_csv(rfc, ip: str, port: str, flag):
    with open(csv_receivedlist, mode='a', newline ='') as myfile:
        wr = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow([str(rfc) +'.txt;' + ip + ';' + str(port) + ';' + flag])

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
    print("1. Registering with RS\n2. Requesting Peer List and RFC's\n3. Leave the network")
    choice = int(input("Enter your request: "))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host_RS,Port_RS))
    if choice == 1:
        registration()
    elif choice == 2:
        requesting_peerlist()
    else:
        leave_message()
        
        