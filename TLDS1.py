# This is code for TLDS1
import socket as mysoc
import hmac
import time


# TLDS1 listens on port 65348 for both AS and CLIENT
# TLDS1 ONLY LISTENS FOR NEW SOCKET CONNECTIONS

class Node:
    def __init__(self, host, ipaddress, flag):
        self.host = host
        self.ipaddress = ipaddress
        self.flag = flag


def normalize(args):
    args.replace('\n', '').replace('\r', '')
    arg1, arg2, arg3 = args.split()
    arg1 = arg1.strip()
    arg2 = arg2.strip()
    arg3 = arg3.strip()
    return arg1, arg2, arg3


def server():
    # This creates a new entry list to append all of the DNS entries to
    Entrytable = []
# open the file for reading, and to scan through the entire document
    with open("PROJ3-TLDS2.txt", "r") as fp:
        for line in fp:
            host, ip, flag = normalize(line)
            node = Node(host, ip, flag)
            Entrytable.append(node)

    # CONNECTION TO AS SERVER
    try:
        AS_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        # print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    AS_PORT = 65348
    as_server_binding = ('', AS_PORT)
    AS_SOCKET.bind(as_server_binding)
    AS_SOCKET.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    as_sockid, addr = AS_SOCKET.accept()
    # print("[S]: Got a connection request from a client at", addr)
    print("tlds1 server connected to as server at port 65348")

# connect to the client
    try:
        client_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        # print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    client_server_binding = ('', 55551)
    client_socket.bind(client_server_binding)
    client_socket.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    c_sockid, addr = client_socket.accept()
    # print("[S]: Got a connection request from a client at", addr)
    print("tlds1 server connected to client at port 55551")

    key = ""
    with open("PROJ3-KEY1.txt", "r") as k:
        for line in k:
            key = line.strip()

    print("[Key]: {}".format(key))

    while True:  # keep getting the challenge from the AS server
        challenge = as_sockid.recv(1024)
        if not challenge:
            break
        challenge = challenge.decode('utf-8')
        print("[TLDS1]: {}".format(challenge))

        d1 = hmac.new(key.encode(), challenge.encode("utf-8")).hexdigest()
        print(d1)
        as_sockid.send(d1.encode('utf-8'))

        time.sleep(1)
# now we wait for a reply from the client
        data = c_sockid.recv(1024)
        data = data.decode('utf-8')
        time.sleep(1)
        print("DATA recieved from client: {}".format(data))

        intable = False
        if data != 'NO':
            for nodes in Entrytable:
                toreturn = ""
                if (nodes.host == data):
                    toreturn = "{} {} {}".format(data, nodes.ipaddress, "A")
                    c_sockid.send(toreturn.encode("utf-8"))
                    print(toreturn)
                    intable = True
            if intable == False:
                error_msg = "ERROR: HOST NOT FOUND\n"
                print(error_msg)
                c_sockid.send(error_msg.encode('utf-8'))


# Close the server socket
    AS_SOCKET.close()
    exit()


server()
