# This is the code for the RS server. We need 3 sockets:
# -to connect to the client and send back the results
# -to connect to TLDS1 server
# -to connect to TLDS2 server
import socket as mysoc
import hmac
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
        print("[TLDS1_SOCKET]: Socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    TLDS1_PORT = 65348
    server_binding = (mysoc.gethostbyname("cpp.cs.rutgers.edu"), TLDS1_PORT)
    TLDS1_SOCKET.connect(server_binding)

    # TLDS2 CONNECTION
    try:
        TLDS2_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TLDS2_SOCKET]: TLDS2_SOCKET socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    TLDS2_PORT = 65349
    server_binding = (mysoc.gethostbyname("java.cs.rutgers.edu"), TLDS2_PORT)
    TLDS2_SOCKET.connect(server_binding)


# AS server will keep receiving strings from the client
# and computing the digest and keep sending it off to both TLDS servers
# Then, it will compare the original digest received from the client to
# the digest received from the TLDS servers.

    while True:
        serialized_data = csockid.recv(1024)
        if not serialized_data:
            break
        deserialized_data = loads(serialized_data)
        challenge = deserialized_data[0]
        as_digest = deserialized_data[1]
        print(challenge, as_digest)

        encoded_challenge = challenge.encode('utf-8')
        TLDS1_SOCKET.send(encoded_challenge)
        print("Sent {} to TLDS1".format(challenge))
        TLDS2_SOCKET.send(encoded_challenge)
        print("Sent {} to TLDS2".format(challenge))

        tlds1_digest = TLDS1_SOCKET.recv(1024).decode('utf-8')
        tlds2_digest = TLDS1_SOCKET.recv(1024).decode('utf-8')

        server_hostname = ""
        if hmac.compare_digest(tlds1_digest, as_digest):
            server_hostname = "cpp.cs.rutgers.edu"
        if hmac.compare_digest(tlds2_digest, as_digest):
            server_hostname = "java.cs.rutgers.edu"

        csockid.send(server_hostname.encode('utf-8'))

    AS_SOCKET.close()
    exit()


server()
