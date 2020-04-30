
import socket
import os
from _thread import *
import threading
import json
import csv
import datetime

file_name = []
file_list = []
file_location = "C:\\IP\\RFCS\\"
file_location.strip()
file_path = file_location + 'E1TR1_S2_R1_001.fastq'
filepath_loc = "C:\\IP\\ips.csv"
filepath = "C:\\IP\\ips.csv"
path = "C:\\IP\\RFCS\\"
  
class pthread(threading.Thread):
    
    def __init__(self,socket,Client_IP):
        threading.Thread.__init__(self)
        self.lock=threading.Lock()
        print(self.lock)
        self.csocket=socket
        self.ip=Client_IP[0]
        self.socket=Client_IP[1]

    def run(self):
        print("Received connection request from:" + threading.currentThread().getName())
        recmsg = self.csocket.recv(2048).decode('utf-8')
        print("Client's message: ", recmsg)

        #client_req = Client_Socket.recv(2048).decode()
        #print(client_req)
        req = json.loads(recmsg)
        print(req)
        Message_type, Hostname, Portnumber = req["msg"], req["Hostname"], req["Portnumber"]

        
        
        if Message_type == 'Requesting_files':
            filename = req["file"]
            print(filename)
            filename = filename.strip()
            print(filename)
            file1 = filename + '.txt'
            print(file1)
            file_path = file_location + '\\'+ file1
            print(file_path) 
            print(file_list)
            if file1 in file_name:
                print("File present")
                fileSize = os.stat(file_path).st_size
                print(fileSize)
                try:
                    f = open (file_path,'rb')  # file opened in binary mode
                    #print
                except:
                    print("Error: Unable to open the file: %s",file_path)
                    errmsg = "404: Not Found"
                    self.csocket.send(errmsg.encode('utf-8'))
                    self.csocket.close()
                    exit()

                x = f.read(2048)
                while (fileSize > 0):
                    self.csocket.send(x)
                    fileSize -= 2048
                    print(fileSize)
                    x = f.read(2048)
                    if((fileSize == 0) or (fileSize<0)):
                        f.close()
                        break
                print("File Sent: %s",file_path)
                self.csocket.close()

            else:
                print("Error: File Not Found: ",file_path)
                errmsg = "404: Not Found"
                self.csocket.send(errmsg.encode('utf-8'))
                self.csocket.close()
                exit()
                

        elif Message_type == 'listofrfcs':
            global filepath_loc
            # Reading the data from the csv file to determine the RFCs present in the system.
            list_of_files = []
            #filepath1 = "C:\\IP1\\ips.csv"
            with open(filepath_loc, 'r') as fil:
                read = csv.reader(fil)
                for record in read:
                    list_of_files.append(record)
            data = json.dumps(list_of_files)
            response = 'Successful' + '\n' + str(datetime.datetime.now()) + '\n' + data
            print(response)
            self.csocket.send(response.encode())
            print("Data Sent")

            """
            l_active = Peerlist.send_AP(server_IP)
            print(l_active)
            #l_active.append({'Date':str(datetime.datetime.now())})
            query_data = json.dumps(l_active)
            print("query data=", query_data)

            # Check if any peer is active or not
            if len(l_active) > 0:
                list_active = '200 OK'+'\n' + query_data
                conn.send(list_active.encode())
                conn.close()
            """
"""
# create  socket object 
s = socket.socket()          
print ("Socket successfully created")
  
# Reserve port number on your system 
port = 8142   
print("Host", socket.gethostbyname(socket.gethostname()))             

# Bind to the port by keeping IP field empty. 
# By doing this, the server is made to listen to requests coming from other systems on network. 
s.bind(('', port))      
print ("socket binded to %s" %(port))
  
# Listen for requests from other system
s.listen(5)      
print ("socket is listening")           
"""
"""
while True: 
  
    # Connect with client. 
    socket_client, IP_client = s.accept()      
    print ('Connected to :', IP_client )
   
    #socket_client.send('Thank you for connecting'.encode('utf-8')) 
    filesize = os.stat(file_path).st_size
    #filename = file_path
    #f = open(filename,'rb')
    f = open(file_path,'rb')
    l = f.read(1024)
    while filesize>0:
        socket_client.send(l)
        filesize -= 1024
        l = f.read(1024)
    f.close()
    print('Done sending')  
    break
socket_client.close()
print("Socket closed")
"""

# Sub routing to get all the RFC files present in the current server.
def get_all_files(path):
    #file_list = []
    global filepath
    basepath = path
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    print(ip)
    s.close()
    port1 = str(port)
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            #print ("asdfasdf")
            print(entry)
            fileName = entry + ';' + ip + ';' + port1 + ';' + '1'
            file_list.append(fileName)
    print(file_list)
    
    # writing all the files in the csv file
    #filepath = "C:\\IP1\\ips.csv"
    print("Storing the RFCs present in the local Server to: ",filepath)
    with open(filepath,'w', newline ='') as f:
        writer = csv.writer(f)
        for words in file_list:
            writer.writerow([words])
     


def get_all_files_names(path):
    #file_name = []
    basepath = path
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    port1 = str(port)
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            print(entry)
            file_name.append(entry)
    print(file_name)

Server_Thread = []
port = 20000
def main():
    global path
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("All the files in the present working directory:")
    #path = "C:\\IP1\\RFCS\\"
    get_all_files(file_location)
    #print("All the files in the present working directory:")
    #path = "C:\\IP1\\RFCS\\"
    get_all_files_names(file_location)
    
    
    #print(file_list) 
    
    Host = ''
    #port = int(global_listening_port)
    
    #Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((Host,port))
    print ("socket binded to %s " %(port))

    while True:
        s.listen(6)
        print('The Server Socket is listening')
        Client_Socket, Client_IP= s.accept()
        print("Client_Scoket", Client_Socket)
        print("IP", Client_IP)
        
        print("Client_Socket: ",Client_Socket)
        print("Got the connection from Client_Socket: ",Client_IP)
        np=pthread(Client_Socket,Client_IP)
        np.start()
        Server_Thread.append(np) 
    
for st in Server_Thread:
	st.join()

main()


