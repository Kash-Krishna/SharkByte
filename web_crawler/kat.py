from bs4 import BeautifulSoup
from urllib2 import HTTPError, URLError
from StringIO import StringIO
import urllib2, sys, sqlite3, time, gzip, re, zlib



if __name__ == "__main__":
    
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #x = 'https://reddit.com' # tested with reddit it works!! 
    url = 'https://kat.cr' #gzip encoding resolved 

    #magical header found on stack overflow that resolved 403
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'gzip',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    query = raw_input("Enter Query to search on ExtraTorrents (press enter to seach on main page): ")
    if query != "":
        #edit url with query
        query = query.replace(" ", "%20")
        print "your query is: " + query
        search_url = url + "/usearch/" + query
    else:
        search_url = url + "/new/"
   
    #testing purposes
    print "Searching: " + search_url + '\n'

    req = urllib2.Request(search_url, headers=hdr)
    http_r = urllib2.urlopen(req)
    #if the responses is gzip encoded, unzip it.
    if http_r.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(http_r.read())
        f = gzip.GzipFile(fileobj=buf)
        r = f.read()
    else:
        r = http_r.read()
    
    http_r.close()
    soup = BeautifulSoup(r)
    #print soup.prettify() #tested kat.cr, works with gzip responses!
    links = set() #all href links from kat page
    torrents = [] #all torrent links, prepend url to go to subpage for torrent files/magnet links
    treasures = [] #includes all found torrents in tuples ready to insert to the database
    
    for anchor in soup.find_all('a'):
        links.add(anchor.get('href','/'))
    
    for l in links:
        #print l
        if ('.html' in l):
            torrents.append(l)
    #testing purposes
    print '------------------------------------------'
    #make Connection with database
    conn  = sqlite3.connect('youtor.db', isolation_level=None)
    conn.text_factory = str
    c = conn.cursor()
    thresh_hold = 10 #used for testing, take the first ten torrents
    torrent_count = 0

    #extract data from eaach sub page of kat
    for t in torrents:
        #print "searching in " + url + t
        req_t = urllib2.Request(url+t, headers= hdr) #extratorrent.cc/torrent/blah
        while True:
            try:
                http_tr = urllib2.urlopen(req_t)
                print "URL open success! at: " + url + t
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

        cat_soup = BeautifulSoup(r_t)
        http_tr.close()

        torrent_name = str(cat_soup.title)
        torrent_name = torrent_name[16:-35]
        print "Torrent Name: " + torrent_name
        
        #kitten is sub sections to get info of the torrent
        kitten_soup = BeautifulSoup(str(cat_soup.find('div',{'class':'torrent_files'})))

        total_size =  kitten_soup.find(text=re.compile('^ \(Size: '))
        byte_size = kitten_soup.find(text=re.compile('\<span\>(K|M|GB)|(bytes)'))

        total_size = total_size[7:] + str(byte_size)
        
        kitten_soup = BeautifulSoup(str(cat_soup.find('div',{'class':'seedLeachContainer'})))
        #print kitten_soup.prettify()
        #break
        seeder = kitten_soup.find('div',{'class','seedBlock'}).find('strong')
        seeder = str(seeder)[8:-9]

        leecher = kitten_soup.find('div',{'class','leechBlock'}).find('strong')
        leecher = str(leecher)[8:-9]
        
        kitten_soup = BeautifulSoup(str(cat_soup.find('div',{'class':'font11px lightgrey line160perc'})))
        try:
            uploader = str(kitten_soup.find('a',{'class':'plain'}).get('href'))
            uploader = uploader[6:-1]
        except:
            print "Error site not accessible"
            continue
        date_and_time = str(kitten_soup.find('time',{'class':'timeago'}).get('datetime'))

        upload_date = date_and_time[:10]
        upload_time = date_and_time[12:19]
        
        date_and_time = upload_date + " " + upload_time

        magnet_link = str(cat_soup.find('a',{'title':'Magnet link'}).get('href'))
                
        #Look for "Download verified torrent file" for torrent files, kat only
        
        #Create tuple with torrent info
        row = (torrent_name, total_size, seeder, leecher, uploader, date_and_time, magnet_link);
        treasures.append(row)
        torrent_count+=1
        c.execute("INSERT OR IGNORE INTO local_youtor VALUES (?,?,?,?,?,?,?)", row);
        print "Digging up sweet loot!\n #" + str(torrent_count) + "! Loot: " + torrent_name
    #end for loop
    print "Total of " + str(torrent_count) + " Torrents found!"
    conn.close

