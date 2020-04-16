
import socket
import os
from _thread import *
import threading
import json
import csv

file_name = []
file_list = []
file_location = "C:\\IP\\RFCS\\"
file_location.strip()
file_path = file_location + 'E1TR1_S2_R1_001.fastq'
filepath1 = "C:\\IP\\ips.csv"
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
        #print(recmsg)
        if 'GetRFC' in recmsg:
            data = recmsg[recmsg.index('GetRFC')+7:recmsg.index('P2P-DI')]
            print(data)
            data = data.strip()
            #print(data)
            file1 = data + '.txt'
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
                

        elif 'RFCQuery' in recmsg:
            global filepath1
            # Reading the data from the csv file to determine the RFCs present in the system.
            list1 = []
            #filepath1 = "C:\\IP1\\ips.csv"
            with open(filepath1, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    list1.append(row)
            data = json.dumps(list1)
            send_response = 'POST 200 OK' + '<cr> <lf>\nFrom:' + socket.gethostname() + '<cr><lf>\nDate:' + str(time.asctime(time.localtime(time.time()))) + '<cr> <lf>\nData-Type: RFClist <cr> <lf>\n<cr> <lf>\n' + data
            print(send_response)
            self.csocket.send(send_response.encode())
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
Server_Thread = []
def main():
    global path
    s = socket.socket()
    print("All the files in the present working directory:")
    #path = "C:\\IP1\\RFCS\\"
    #get_all_files(path)
    #print("All the files in the present working directory:")
    #path = "C:\\IP1\\RFCS\\"
    #get_all_files_names(path)
    
    
    #print(file_list) 
    
    Host = ''
    #port = int(global_listening_port)
    port = 8143
    #Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((Host,port))
    print ("socket binded to %s " %(port))

    while True:
        s.listen(6)
        print('The Server Socket is listening')
        Client_Socket, Client_IP= s.accept()
        print("Client_Socket: ",Client_Socket)
        print("Got the connection from Client_Socket: ",Client_IP)
        np=pthread(Client_Socket,Client_IP)
        np.start()
        Server_Thread.append(np) 
    
for st in Server_Thread:
	st.join()

main()


