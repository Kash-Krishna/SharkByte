import os

os.system("sudo apt-get -y update")
#os.system("")
sources = open("/etc/apt/sources.list","a")
sources.write("deb http://deb.torproject.org/torproject.org jessie main")
sources.write("deb-src http://deb.torproject.org/torproject.org jessie main")
os.system("sudo gpg --keyserver keys.gnupg.net --recv 886DDD89")
os.system("sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -")
sources.close()
os.system("sudo apt-get install -y tor")

os.system("sudo service tor start")
os.system("sudo systemctl enable tor")

torrc = open("/etc/tor/torrc", "a")
torrc.write("VirtualAddrNetworkIPv4 10.192.0.0/10\nAutomapHostsOnResolve 1\nTransPort 9040\nDNSPort 53\n")
torrc.close()
#with open("/etc/resolv.conf", "a") as f: f.write("nameserver 127.0.0.1\n")
os.system("./torifyIPTables.sh")

