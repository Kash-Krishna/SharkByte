from bs4 import BeautifulSoup
from urllib2 import HTTPError, URLError
from StringIO import StringIO
import urllib2, sys, sqlite3, time, gzip, re, zlib

def search_kat(query, hdr):
    
    reload(sys)
    sys.setdefaultencoding('utf-8')

    #x = 'https://reddit.com' # tested with reddit it works!! 
    url = 'https://kat.cr' #gzip encoding resolved 

    #getting rid of raw input to get query pass in through args
    #query = raw_input("Enter Query to search on ExtraTorrents (press enter to seach on main page): ")
    if query != "":
        #edit url with query
        query = query.replace(" ", "%20")
        search_url = url + "/usearch/" + query
    else:
        search_url = url + "/linux/?field=seeders&sorder=desc"
   
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
    links = set() #all href links from kat page
    torrents = [] #all torrent links, prepend url to go to subpage for torrent files/magnet links
    treasures = [] #includes all found torrents in tuples ready to insert to the database
    
    for anchor in soup.find_all('a'):
        links.add(anchor.get('href','/'))
    
    for l in links:
        if ('.html' in l):
            torrents.append(l)
    #make Connection with database
    db_conn  = sqlite3.connect('../torrents.db', isolation_level=None)
    db_conn.text_factory = str
    cursor = db_conn.cursor()
    torrent_count = 0

    #extract data from eaach sub page of kat
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

        cat_soup = BeautifulSoup(r_t)
        http_tr.close()

        torrent_name = str(cat_soup.title)
        torrent_name = torrent_name[16:-35]

        #kitten is sub sections to get info of the torrent
        kitten_soup = BeautifulSoup(str(cat_soup.find('div',{'class':'torrent_files'})))

        total_size =  kitten_soup.find(text=re.compile('^ \(Size: '))
        tiny_kat = BeautifulSoup(str(kitten_soup.find('span',{'class':'folderopen'})))
        byte_size = tiny_kat.findAll('span')[2]
        byte_size = str(byte_size)[6:-7]
        
        total_size = total_size[7:] + byte_size
        #print total_size
        #resoup
        kitten_soup = BeautifulSoup(str(cat_soup.find('div',{'class':'seedLeachContainer'})))

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
        cursor.execute("INSERT OR IGNORE INTO local_youtor VALUES (?,?,?,?,?,?,?)", row);
    #end for loop
    conn.close

    print "Total of " + torrent_count + " torrents"


if __name__ == '__main__':

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1, utf-8; q=0.7,*q=0.3',
       'Accept-Encoding': 'gzip',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection':'keep-alive'
      }
    
    search_kat("", hdr)
