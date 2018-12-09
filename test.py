import hmac
import json
import pickle
c1 = "arianna"
c2 = "grande"
d1 = hmac.new("k3521".encode(), c1.encode("utf-8"))
d2 = hmac.new("k3522".encode(), c1.encode("utf-8"))
d3 = hmac.new("k3521".encode(), c1.encode("utf-8"))
d4 = hmac.new("k3521".encode(), c2.encode("utf-8"))


def normalize(args):
    args.replace('\n', '').replace('\r', '')
    key, challenge, hostname = args.split()
    key = key.strip()
    challenge = challenge.strip()
    hostname = hostname.strip()
    return key, challenge, hostname

    # print(key, challenge, hostname)


with open("PROJ3-HNS.txt", "r") as file_handler:
    for line in file_handler:
        key, challenge, hostname = normalize(line)
        # print(key, challenge, hostname)
        digest = hmac.new(key.encode(), challenge.encode("utf-8")).hexdigest()
        serialized_data = pickle.dumps([key, challenge], -1)
        # print(pickle.dumps()
        # print("Line: {}Digest: {}".format(line, digest))

# fh.close()
