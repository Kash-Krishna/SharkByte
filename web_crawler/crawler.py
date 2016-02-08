from bs4 import BeautifulSoup
import urllib2
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    
    #x = 'https://reddit.com' # tested with reddit it works!! 
    x = 'http://extratorrent.cc'
    #magical header found on stack overflow
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
    torrents = []
    page_contents = []
    for anchor in soup.find_all('a'):
        links.append(anchor.get('href','/'))
        #print(anchor.get('magnet:?')
    for l in links:
        if ('/torrent/' in l):
            torrents.append(l)
    for t in torrents:
        req_t = urllib2.Request(x+t, headers= hdr) #extratorrent.cc/torrent/blah
        r_t = urllib2.urlopen(req_t).read()
        turtle_soup = BeautifulSoup(r_t)
        
        print "Seeder: " + ''.join(turtle_soup.find(text='Seeds:').next.findAll(text=True))
        
        print "Leecher: " + ''.join(turtle_soup.find(text='Leechers:').next.findAll(text=True))
        
        print "Uploader: " + ''.join(turtle_soup.find(text='Uploader:').next.findAll(text=True))
        
        print "Filename: " + ''.join(turtle_soup.find(text='Download torrent:').next.findAll(text=True))

        print "Total Size: " + ''.join(turtle_soup.find(text='Total Size:').next.findAll(text=True))
        
        date =''.join(turtle_soup.find(text='Torrent added:').next.findAll(text=True))
        print "Upload Date & Time: " + date[:20]
        
        for lk in turtle_soup.findAll('a',href=True,title=True):
            if lk['title'] == "Magnet link":
                print "Magnet Link: " + lk['href']

        print '---------------------------------------------'
