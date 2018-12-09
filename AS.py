# This is the code for the RS server. We need 3 sockets:
# -to connect to the client and send back the results
# -to connect to TLDS1 server
# -to connect to TLDS2 server
import socket as mysoc


def server():
    # connect to TLDS1
    try:
        cs1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port = 65348
    server_binding = (mysoc.gethostbyname("cpp.cs.rutgers.edu"), port)
    cs1.connect(server_binding)
# connect to TLDS2
    try:
        cs2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port = 65349
    server_binding = (mysoc.gethostbyname("java.cs.rutgers.edu"), port)
    cs2.connect(server_binding)
# socket to connect to the client
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 65347)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)
# AS server will keep receiving strings from the client
# and computing the digest and keep sending it off to both TLDS servers
# Then, it will compare the original digest received from the client to
# the digest received from the TLDS servers.

    while True:
        challenge = csockid.recv(1024)  # receive challenge from client
        if not challenge:
            break
        challenge = challenge.decode('utf-8')
        challenge = challenge.strip()
        digest = csockid.recv(1024)  # receive the digest from client
        digest = digest.decode('utf-8')
        digest = digest.strip()
        server = ""
# send challenge to TLDS1, receive a digest
        cs1.send(challenge.encode('utf-8'))
        digest1 = cs1.recv(1024)
        digest1 = digest1.decode('utf-8')
# send digest to TLDS2, receive a digest
        cs2.send(challenge.encode('utf-8'))
        digest2 = cs2.recv(1024)
        digest2 = digest2.decode('utf-8')
# compare the digests to the original digest recv from the client
        if (digest1 == digest):  # digest match is in TLDS1
            server = "TLDS1"

        if (digest2 == digest):  # digest match is in TLDS2
            server = "TLDS2"
# send the client the server string back
        csockid.send(server.encode('utf-8'))

# Close the server socket
    #input("Press ENTER to close server socket and end the program.")
    ss.close()
    exit()


server()
