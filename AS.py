# This is the code for the RS server. We need 3 sockets:
# -to connect to the client and send back the results
# -to connect to TLDS1 server
# -to connect to TLDS2 server
import socket as mysoc
import hmac
import time
from pickle import dumps, loads

# AS listens on port 65347 for CLIENT
# AS CREATES SOCKET on port 65348 for TLDS1
# AS CREATES SOCKET on port 65349 for TLDS2


def server():
    # CLIENT CONNECTION

    try:
        AS_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.errnr as err:
        print('{}'.format('socket open error', err))

    CLIENT_PORT = 65347
    as_binding = ('', CLIENT_PORT)
    AS_SOCKET.bind(as_binding)
    AS_SOCKET.listen(1)
    host = mysoc.gethostname()
    print("[AS]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[AS]: Server IP address is  ", localhost_ip)
    csockid, addr = AS_SOCKET.accept()
    print("[AS]: Got a connection request from a client at", addr)

    # TLDS1 CONNECTION
    try:
        TLDS1_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        # print("[TLDS1_SOCKET]: TLDS1_SOCKET Socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    TLDS1_PORT = 65348
    tlds1_hostname = mysoc.gethostbyname("cpp.cs.rutgers.edu")
    tlds1_server_binding = (tlds1_hostname, TLDS1_PORT)
    TLDS1_SOCKET.connect(tlds1_server_binding)
    print("AS SERVER connected to tlds1")

    # TLDS2 CONNECTION
    try:
        TLDS2_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        # print("[TLDS2_SOCKET]: TLDS2_SOCKET socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    TLDS2_PORT = 65349
    tlds2_hostname = mysoc.gethostbyname("java.cs.rutgers.edu")
    tlds2_server_binding = (tlds2_hostname, TLDS2_PORT)
    TLDS2_SOCKET.connect(tlds2_server_binding)
    print("AS SERVER connected to tlds2\n")


# AS server will keep receiving strings from the client
# and computing the digest and keep sending it off to both TLDS servers
# Then, it will compare the original digest received from the client to
# the digest received from the TLDS servers.

    while True:
        serialized_data = csockid.recv(1024)
        if not serialized_data:
            break
        deserialized_data = serialized_data.decode("utf-8").split(";")
        # print("Message recieved from client", deserialized_data)
        challenge = deserialized_data[0]
        as_digest = deserialized_data[1]
        print("{} {}".format(challenge, as_digest))

        encoded_challenge = challenge.strip().encode('utf-8')

        TLDS1_SOCKET.send(encoded_challenge)
        # print("Sending {} to tlds1".format(encoded_challenge))
        time.sleep(1)

        TLDS2_SOCKET.send(encoded_challenge)
        # print("Sending {} to tlds2".format(encoded_challenge))
        time.sleep(1)

        tlds1_data = TLDS1_SOCKET.recv(1024)
        tlds1_digest = tlds1_data.decode('utf-8')
        print("[TLDS1 Digest]: {}".format(tlds1_digest))

        tlds2_data = TLDS2_SOCKET.recv(1024)
        tlds2_digest = tlds2_data.decode('utf-8')
        print("[TLDS2 Digest]: {}".format(tlds2_digest))

        # server_hostname = ""
        if as_digest == tlds1_digest:
            csockid.send("TLDS1".encode('utf-8'))

        elif as_digest == tlds2_digest:
            csockid.send("TLDS2".encode('utf-8'))

            # server_hostname = "java.cs.rutgers.edu"

        # csockid.send(server_hostname.encode('utf-8'))

    AS_SOCKET.close()
    TLDS1_SOCKET.close()
    TLDS2_SOCKET.close()
    exit()


server()
