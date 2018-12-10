import socket as mysoc
import hmac
import time
from cPickle import dumps, loads

# CLIENT CREATES SOCKETS TO TLDS1 ON 65348
# CLIENT CREATES SOCKETS TO TLDS2 ON 65349


def normalize(args):
    args.replace('\n', '').replace('\r', '')
    arg1, arg2, arg3 = args.split()
    arg1 = arg1.strip()
    arg2 = arg2.strip()
    arg3 = arg3.strip()
    return arg1, arg2, arg3


def client():
    # connect to the AS root server to send all the queries to
    try:
        AS_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    AS_PORT = 65347
    strhost = mysoc.gethostbyname(mysoc.gethostname())
    server_binding = (strhost, AS_PORT)
    AS_SOCKET.connect(server_binding)

    time.sleep(1)
    # connect to TLDS1
    try:
        TLDS1_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TLDS1]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    TLDS1_PORT = 55551
    ts1_host = mysoc.gethostbyname("cpp.cs.rutgers.edu")
    ts1_server_binding = (ts1_host, TLDS1_PORT)
    TLDS1_SOCKET.connect(ts1_server_binding)
    print("client connected to tlds1")

    time.sleep(1)

    # connect to TLDS2
    try:
        TLDS2_SOCKET = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TLDS2]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    TLDS2_PORT = 55552
    ts2_host = mysoc.gethostbyname("java.cs.rutgers.edu")
    ts2_server_binding = (ts2_host, TLDS2_PORT)
    TLDS2_SOCKET.connect(ts2_server_binding)
    print("client connected to tlds2")

    time.sleep(1)

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
            if not line:
                break

            key, challenge, hostname = normalize(line)
            # print(key, challenge, hostname)
            digest = hmac.new(key.encode(), challenge.encode('utf-8'))
            digest = digest.hexdigest()

            broker = "{};{}".format(challenge, digest).strip()
            print(broker)

            AS_SOCKET.send(broker.encode("utf-8"))
            time.sleep(1)
            as_response = AS_SOCKET.recv(1024)
            as_response = as_response.decode("utf-8").strip()
            print("Recieved from AS Server: ", as_response)

            result = ""
            if as_response == "TLDS1":
                TLDS1_SOCKET.send(hostname.encode('utf-8'))
                TLDS2_SOCKET.send("NO".encode('utf-8'))
                result = TLDS1_SOCKET.recv(1024)
                result = result.decode('utf-8')
                result = result.strip()
                result = "{} {}\n".format(as_response, result)
                print("WRITE: {}".format(result))
                output.write(result)

            elif as_response == "TLDS2":
                TLDS2_SOCKET.send(hostname.encode('utf-8'))
                TLDS1_SOCKET.send("NO".encode('utf-8'))
                result = TLDS2_SOCKET.recv(1024)
                result = result.decode('utf-8')
                result = result.strip()
                result = "{} {}\n".format(as_response, result)
                print("WRITE: {}".format(result))
                output.write(result)

    print("Results have been written to RESOLVED.txt.")
    AS_SOCKET.close()
    TLDS1_SOCKET.close()
    TLDS2_SOCKET.close()
    exit()


client()
