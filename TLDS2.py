# This is code for TLDS1
import socket as mysoc
import hmac


class Node:
    def __init__(self, host, ipaddress, flag):
        self.host = host
        self.ipaddress = ipaddress
        self.flag = flag


def server():
    # This creates a new entry list to append all of the DNS entries to
    Entrytable = []
# open the file for reading, and to scan through the entire document
    f = open("PROJ3-TLDS2.txt", "r")
    for line in f:
        x = line
# split the line into its respective three parts
# make a new node out of it, and add it to the TLDS1 table
        host, ip, flag = x.split()
        host = host.strip()
        ip = ip.strip()
        flag = flag.strip()
        tmp = Node(host, ip, flag)
        Entrytable.append(tmp)

# connect to the AS server
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 60002)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)

# connect to the client
    try:
        so = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 65349)
    so.bind(server_binding)
    so.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid2, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)

    k = open("PROJ3-KEY2.txt", "r")
    key = ""

    for line in k:
        key = line

    while True:  # keep getting the challenge from the AS server
        challenge = csockid.recv(1024)
        if not challenge:
            break
        challenge = challenge.decode('utf-8')
        challenge = challenge.strip()
# now that we got the challenge string- create the digest
        d1 = hmac.new(key.encode(), challenge.encode())
        csockid.send(d1.encode('utf-8'))
# now we wait for a reply from the client
        data = csockid2.recv(1024)
        data = data.decode('utf-8')
        if (data != "NO"):  # search the table for a match
            for nodes in Entrytable:
                if (nodes.host == data):
                    intable = True
                    toreturn = data + " " + nodes.ipaddress + " A"
                    print(data + " " + nodes.ipaddress + " A")
# this means that the name does not exist in the TS table-
        if (intable == False):
            toreturn = data + "- Error: HOST NOT FOUND"
            print(data + " - Error: HOST NOT FOUND")

        csockid2.send(toreturn.encode('utf-8'))


# Close the server socket
    ss.close()
    exit()


server()
