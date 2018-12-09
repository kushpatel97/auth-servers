import socket as mysoc
import hmac


def normalize(args):
    args.replace('\n', '').replace('\r', '')
    key, challenge, hostname = args.split()
    key = key.strip()
    challenge = challenge.strip()
    hostname = hostname.strip()
    return key, challenge, hostname


def client():
    # connect to the AS root server to send all the queries to
    try:
        AS_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port = 65347
    strhost = mysoc.gethostbyname(mysoc.gethostname())
    # roothost=input("Enter the hostname of the root server: \n")
    server_binding = (strhost, port)
    AS_SOCKET.connect(server_binding)

    # connect to TLDS1
    try:
        TLDS1_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port = 65348
    # TS1host=input("Enter the hostname of 1st authentication server \n")
    ts1_host = mysoc.gethostbyname("cpp.cs.rutgers.edu")
    TS1_bind = (ts1_host, 65348)
    TLDS1_SOCKET.connect(TS1_bind)
    print("[TLDS1]: Connected")

    # connect to TLDS2
    try:
        TLDS2_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port = 65349
    # TS2host=input("Enter the hostname of 2nd authentication server \n")

    ts2_host = mysoc.gethostbyname("java.cs.rutgers.edu")

    TS2_bind = (ts2_host, 65349)
    TLDS2_SOCKET.connect(TS2_bind)
    print("[TLDS2]: Connected")

    # f = open("PROJ3-HNS.txt", "r")

    output = open("RESOLVED.txt", "w")

    # go through the file and send each line to the AS server.
    # AS server will take care of finding the appropriate server
    # go through every line in the doc- break up into its three parts:
    # key, challenge, and hostname (lines 55-59)
    # create digest (line 60)
    # send to AS server, and then wait for response (lines 62-63)
    # then search for the hostname in the appropriate TS server (lines 62-72)

    with open("PROJ3-HNS.txt", "r") as fp:
        for line in fp:
            key, challenge, hostname = normalize(line)
            digest = hmac.new(key.encode(), challenge.encode('utf-8')).hexdigest())

    for line in f:
        x=line
        key, challenge, hostname=x.split()
        key=key.strip()
        challenge=challenge.strip()
        hostname=hostname.strip()
        digest=hmac.new(key.encode(), challenge.encode("utf-8"))
# now that digest has been made- send challenge and digest to AS
        AS_SOCKET.send(challenge.encode('utf-8'))
        AS_SOCKET.send(digest.encode('utf-8'))
        server=AS_SOCKET.recv(1024)  # which server to send request to
        result=""  # what we get from the server

        if (server == "TLDS1"):
            TLDS1_SOCKET.send(hostname.encode('utf-8'))
            TLDS2_SOCKET.send("NO".encode('utf-8'))
            result=TLDS1_SOCKET.recv(1024)
            result=result.decode('utf-8')
            result=result.strip()

        if (server == "TLDS2"):
            TLDS2_SOCKET.send(hostname.encode('utf-8'))
            TLDS1_SOCKET.send("NO".encode('utf-8'))
            result=TLDS2_SOCKET.recv(1024)
            result=result.decode('utf-8')
            result=result.strip()

        if (result == "False"):
            output.write(server + " " + hostname +
                         " - Error: HOST NOT FOUND\n")

        else:
            output.write(server + " " + hostname + " " + result + " A\n")
# close the client socket
    print("Results have been written to RESOLVED.txt.")
    AS_SOCKET.close()
    exit()


client()