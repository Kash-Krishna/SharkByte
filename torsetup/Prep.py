import os

with open("/etc/resolv.conf", "a") as f: f.write("nameserver 127.0.0.1\n")
os.system("./torifyIPTables.sh")

