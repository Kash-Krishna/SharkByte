from bs4 import BeautifulSoup
import urllib2

if __name__ == "__main__":
    
    #x = 'https://reddit.com' # tested with reddit it works!! 
    x = 'http://extratorrent.cc/'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    req = urllib2.Request(x, headers=hdr)
    r = urllib2.urlopen(req).read()
    soup = BeautifulSoup(r)
    #print(soup.prettify())
    links = []
    for anchor in soup.find_all('a'):
        links.append(anchor.get('href','/'))
        #print(anchor.get('magnet:?')
    for l in links:
        if (l.find('http')):
            print l
