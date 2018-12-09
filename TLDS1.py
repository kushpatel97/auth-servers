# This is code for TLDS1
import socket as mysoc
import hmac


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
    with open("PROJ3-TLDS1.txt", "r") as fp:
        for line in fp:
            host, ip, flag = normalize(line)
            node = Node(host, ip, flag)
            Entrytable.append(node)
    x = [(node.host, node.ipaddress, node.flag) for node in Entrytable]
    print(x)

    # f = open("PROJ3-TLDS1.txt", "r")
#     for line in f:
#         x = line
#     # split the line into its respective three parts
# # make a new node out of it, and add it to the TLDS1 table
#         host, ip, flag = x.split()
#         host = host.strip()
#         ip = ip.strip()
#         flag = flag.strip()
#         tmp = Node(host, ip, flag)
#         Entrytable.append(tmp)

    # CONNECTION TO AS SERVER
    try:
        AS_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    AS_PORT = 65348
    server_binding = ('', AS_PORT)
    AS_SOCKET.bind(server_binding)
    AS_SOCKET.listen(1)
    host = mysoc.gethostname()

    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    as_sockid, addr = AS_SOCKET.accept()
    print("[S]: Got a connection request from a client at", addr)

# connect to the client
    try:
        so = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 70000)
    so.bind(server_binding)
    so.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    c_sockid, addr = AS_SOCKET.accept()
    print("[S]: Got a connection request from a client at", addr)

    key = ""
    with open("PROJ3-KEY1.txt", "r") as k:
        for line in k:
            key = line.strip()

    while True:  # keep getting the challenge from the AS server
        challenge = as_sockid.recv(1024)
        if not challenge:
            break
        challenge = challenge.decode('utf-8').strip()
        # challenge = challenge.strip()
# now that we got the challenge string- create the digest
        d1 = hmac.new(key.encode(), challenge.encode()).hexdigest()
        as_sockid.send(d1.encode('utf-8'))
# now we wait for a reply from the client
        data = c_sockid.recv(1024)
        data = data.decode('utf-8')

        if data:  # search the table for a match
            for nodes in Entrytable:
                if (nodes.host == data):
                    intable = True
                    toreturn = data + " " + nodes.ipaddress + " A"
                    print(data + " " + nodes.ipaddress + " A")
# this means that the name does not exist in the TS table-
        if (intable == False):
            toreturn = data + "- Error: HOST NOT FOUND"
            print(data + " - Error: HOST NOT FOUND")

        c_sockid.send(toreturn.encode('utf-8'))


# Close the server socket
    AS_SOCKET.close()
    exit()


server()
