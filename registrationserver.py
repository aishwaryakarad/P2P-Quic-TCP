import socket
import time
import json
import datetime

class peers:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.next = None

    def initial(self,IP):
        self.ip = IP
        self.flag = True

class peer_linked_list:
    def __init__(self):
        self.head = peers(None, None)

    def upd(self, host, port, IP):
        current_node = self.head
        while current_node.next != None:
            current_node = current_node.next
            # If the peer has already contacted RS before
            if current_node.hostname == host and current_node.port == port:
                current_node.ip = IP
                return
        # New peer is added to the network
        current_node.next = peers(host,port)
        current_node.ip = IP
        return

    # prepare a list of active peers
    def send_AP(self, IP):
        current_node = self.head
        dictn = {}
        list_d= []
        
        while current_node.next != None:
            current_node = current_node.next

            # If the peer being checked is still active and 
            # the IP is not same as the IP of the peer who requests the info then 
            # add the details to the dictionary
            if (current_node.flag == True and current_node.s_ip != IP):
                dictn = {
                    'ip': current_node.ip,
                    'port': current_node.port
                }
                list_d.append(dictn.copy())
        return list_d

    def leave(self, hostname, port):
        current_node = self.head
        while current_node.next!= None:
            current_node = current_node.next
            if current_node.hostname == host and current_node.port == port:
                current_node.flag=False


    
Peerlist = peer_linked_list()
server_port = 23471
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', server_port))

# Allow maximum 5 pending request
server_socket.listen(5)   
print("Registration server ready")

while True:
    print("Reached here")
    conn, address = server_socket.accept()
    server_IP = address[0]
    req = conn.recv(2048).decode()
    print('#############################REQUEST RECEIVED #############################')
    print(req)
    # Extract the host part from the request
    Hostname = req[req.index('Hostname') + 9:req.index(' <cr> <lf>\nPortnumber')]
    # Extract the port number from the request
    Portnumber = req[req.index('Portnumber') + 11:req.index(' <cr> <lf>\n')]
    # Extract cookie information from the request
    #Cookie_id = req[req.index('Cookie_id') + 10:request.index(' <cr> <lf>')]
    
    # Check the message sent by peer and decide which function of RS needs to be executed

    # 1- peer wants to register and get into the network.
    if 'Register_to_RS' in req:
        Peerlist.upd(Hostname, Portnumber, server_IP)
        response = '200 OK' + '<cr> <lf>\nFrom:' + socket.gethostname() + '<cr><lf>\nDate:' + str(datetime.datetime.now()) + '<cr> <lf>'
        conn.send(response.encode())
        conn.close()

    elif 'Active_peer' in req:
        l_active = peers.send_AP(server_IP)
        query_data = json.dumps(l_active)

        # Check if any peer is active or not

        if len(l_active) > 0:
            list_active = '200 OK' + '<cr> <lf>\nFrom:' + socket.gethostname() + '<cr><lf>\nDate:' + str(datetime.datetime.now()) + '<cr> <lf>\n<cr> <lf>\n' + query_data
         
            conn.send(list_active.encode())
            conn.close()
        else:
            list_active = '404 No Active Peer' + '<cr> <lf>\nFrom:' + socket.gethostname() + '<cr><lf>\nDate:' + str(datetime.datetime.now()) + '<cr> <lf>\n<cr> <lf>\n' + query_data
        
            conn.send(send_Activelist.encode())
            conn.close()

    elif 'Leave_RS' in req:
        Peerlist.leave(Hostname, Portnumber)
        Leave_message = '200 OK' + '<cr> <lf>\nFrom:' + socket.gethostname() + '<cr><lf>\nDate:' + str(datetime.datetime.now()) + '<cr> <lf>\n<cr> <lf>\n' + 'Left successfully'
    
        conn.send(Leave_message.encode())
        conn.close()


