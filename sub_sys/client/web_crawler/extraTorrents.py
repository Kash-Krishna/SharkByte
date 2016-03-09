from bs4 import BeautifulSoup
from urllib2 import HTTPError, URLError
from StringIO import StringIO
import urllib2, sys, sqlite3, time, gzip, re, zlib

def search_extra_t(query, hdr):

    #x = 'https://reddit.com' # tested with reddit it works!! 
    url = 'https://extratorrent.cc'
    #getting rid of raw input query 
    #query = raw_input("Enter Query to search on ExtraTorrents (press enter to seach on main page): ")
    if query != "":
        #replace ' ' in query to '+'
        query = query.replace(" ", "+")
        search_url = url + "/search/?search=" + query + "&new=1&x=0&y=0"
    else:
        search_url = url

    req = urllib2.Request(search_url, headers=hdr)
    http_r = urllib2.urlopen(req)
    if http_r.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(http_r.read())
        f = gzip.GzipFile(fileobj=buf)
        r = f.read()
    else:
        r = http_r.read()

    http_r.close()
    soup = BeautifulSoup(r)
    links = [] #all href links from extratorrents main page
    torrents = [] #all torrent links, prepend url to go to subpage for torrent files/magnet links
    treasures = [] #includes all found torrents in tuples ready to insennrt to the database

    for anchor in soup.find_all('a'):
        links.append(anchor.get('href','/'))
        
    for l in links:
        if ('/torrent/' in l):
            torrents.append(l)
    #make Connection with database
    conn  = sqlite3.connect('../torrents.db', isolation_level=None)
    c = conn.cursor()
    i = 0 #use to ignore firt 20 links(ads) in extratorrent
    torrent_count = 0
    
    #extract data from each torrent sub_page 
    for t in torrents:
        req_t = urllib2.Request(url+t, headers= hdr) #extratorrent.cc/torrent/blah
        while True:
            try:
                http_tr = urllib2.urlopen(req_t)
                time.sleep(1)
                break
            except HTTPError, error_num:
                #output error message
                print "Error! " + str(error_num) + "\n\tAt: " + url + t
        
        if http_tr.info().get('Content-Encoding') == 'gzip':
            t_buf = StringIO(http_tr.read())
            t_f = gzip.GzipFile(fileobj=t_buf)
            r_t = t_f.read()
        else:
            r_t = http_tr.read()

        turtle_soup = BeautifulSoup(r_t)
        http_tr.close()
        
        #skip the first 20 torrents, they're from the sidebar ads
        if i < 20:
            i+=1
            continue

        torrent_name = ''.join(turtle_soup.find(text='Download torrent:').next.findAll(text=True))
        torrent_name = torrent_name.replace(u'\xa0', u' ')
        
        total_size = ''.join(turtle_soup.find(text='Total Size:').next.findAll(text=True))
        total_size = total_size.replace(u'\xa0', u' ')
        
        seeder = ''.join(turtle_soup.find(text='Seeds:').next.findAll(text=True))
        seeder = seeder.replace(u'\xa0', u' ')
        
        leecher = ''.join(turtle_soup.find(text='Leechers:').next.findAll(text=True))
        leecher = leecher.replace(u'\xa0', u' ')
        
        uploader = ''.join(turtle_soup.find(text='Uploader:').next.findAll(text=True))
        uploader = uploader.replace(u'\xa0', u' ')
        
        date_and_time =''.join(turtle_soup.find(text='Torrent added:').next.findAll(text=True))
        date_and_time = date_and_time.replace(u'\xa0', u' ')

        upload_date = date_and_time[:10]
        upload_time = date_and_time[11:20]
        
        date_and_time = upload_date + " " + upload_time
        magnet_link = ""
        
        #look for the right link; magnet links have "Magnet link" in title tag.
        for lk in turtle_soup.findAll('a',href=True,title=True):
            if lk['title'] == "Magnet link":
                magnet_link = lk['href']
        
        #Create tuple with torrent info
        row = (torrent_name, total_size, seeder, leecher, uploader, date_and_time, magnet_link);
        treasures.append(row)
        torrent_count+=1
        time.sleep(1)
        c.execute("INSERT OR IGNORE INTO local_youtor VALUES (?,?,?,?,?,?,?)", row);
    #end for loop
    conn.close
    print "Total of " + torrent_count + " torrents"
