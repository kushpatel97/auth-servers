import hmac
import json
import socket as mysoc
from cPickle import dumps, loads
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


def test():
    with open("PROJ3-HNS.txt", "r") as file_handler:
        for line in file_handler:
            key, challenge, hostname = normalize(line)
            # print(key, challenge, hostname)
            digest = hmac.new(
                key.encode(), challenge.encode("utf-8")).hexdigest()
            serialized_data = dumps([challenge, digest], -1)
            # print(serialized_data)
            # print(hmac.compare_digest())
            deserialized_data = loads(serialized_data)
            print(
                "Challenge: {} --> Digest: {}".format(deserialized_data[0], deserialized_data[1]))


if __name__ == "__main__":
    # print(mysoc.gethostbyname("cpp.cs.rutgers.edu"))
    # print(mysoc.gethostbyname("java.cs.rutgers.edu"))

    test()
