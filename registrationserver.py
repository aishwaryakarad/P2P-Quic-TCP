# Import the required packages
import socket
import time
import json
import datetime

class peers:
    # Contructor
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.next = None
        self.flag = False
        self.ip = None

    # Initial state of the peer
    def initial(self,IP):
        self.ip = IP
        self.flag = True
    
#Create  linkedlist with peer information
class peer_linked_list:
    def __init__(self):
        self.head = peers(None, None)

    # function to check if the peer is already in the network, if yes, update the IP, else add the peer to the network
    def upd(self, host, port, IP):
        new_node = peers(host,port)
        current_node = self.head
        while current_node.next != None:
            current_node = current_node.next
            # If the peer has already contacted RS before
            if current_node.hostname == host and current_node.port == port:
                current_node.ip = IP
                return
        # New peer is added to the network
        current_node.next = new_node
        current_node.next.ip = IP
        current_node.next.flag = True
        return

    # function to prepare a list of active peers
    def send_AP(self, IP):
        current_node = self.head
        dictn = {}
        list_d= []
        
        while current_node.next != None:
            current_node = current_node.next
            print(current_node.hostname)
            print(current_node.flag)

            # If the peer being checked is still active and 
            # the IP is not same as the IP of the peer who requests the info then 
            # add the details to the dictionary
            print(current_node.flag, current_node.ip, current_node.hostname, current_node.port, IP)
            if (current_node.flag == True and current_node.ip != IP):
                dictn = {
                    'ip': current_node.ip,
                    'port': current_node.port
                }
                list_d.append(dictn.copy())
        return list_d

    # Function to leave the network
    def leave(self, host, port):
        current_node = self.head
        while current_node.next!= None:
            current_node = current_node.next
            if current_node.hostname == host and current_node.port == port:
                current_node.flag=False


# Create an object   
Peerlist = peer_linked_list()
# Set port number for RS
server_port = 23473
#Create a TCP socket for RS
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', server_port))

# Allow maximum 5 pending request
server_socket.listen(5)   
print("Registration server ready")

while True:
    #print("Reached here")
    conn, address = server_socket.accept()
    server_IP = address[0]
    print(server_IP)
    request_format = conn.recv(2048).decode()
    req = json.loads(request_format)
    print('#############################REQUEST RECEIVED #############################')
    print(req)
    # Extract the host part from the request
    Message_type, Hostname, Portnumber = req["msg"], req["Hostname"], req["Portnumber"]
    
    # Check the message sent by peer and decide which function of RS needs to be executed

    # 1- peer wants to register and get into the network.
    if Message_type == 'Register_to_RS':
        Peerlist.upd(Hostname, Portnumber, server_IP)
        response = json.dumps({"msg" : '200 OK'})
        conn.send(response.encode())
        conn.close()

    # 2- peer wants to know the list of active peers.
    elif Message_type == 'Active_peer':
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

        # No peer is active
        else:
            list_active = '404 No Active Peer'
            conn.send(list_active.encode())
            conn.close()

    # 3- peer wants to leave the network.
    elif Message_type == 'Leave_the_server':
        Peerlist.leave(Hostname, Portnumber)
        Leave_message = 'Left successfully' + '\nDate:' + str(datetime.datetime.now())
        conn.send(Leave_message.encode())
        conn.close()