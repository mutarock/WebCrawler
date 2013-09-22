# -*- coding: UTF-8 -*-
import urllib, urllib2, re, os, sys, httplib, socket
import robotparser #for check a wbe page can be fetched or not
from urlparse import urljoin #for combine the link

# download link @ http://www.crummy.com/software/BeautifulSoup/download/3.x/
# run in command "python setup.py install" to finish setup
from BeautifulSoup import BeautifulSoup


from urllib2 import urlopen,Request
import urlparse
import httplib
import time  


# use UTF-8 to be the encode mode
reload(sys)
sys.setdefaultencoding('utf8')


'''
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
'''


# download the website
def http_download(url):
    filename = str(len(GLOBAL_ALL_VISIT_QUEUE)) +".html"
    #filename = str(GLOBAL_CUR_PAGE) +".html"
    try:
        file = urllib.urlretrieve(url, work_path + "/" + filename)
        size = os.path.getsize(work_path + "/" + filename)
        return size
    except IOError, e:
        print "***** connect IOError(104) *****"
        print e
        size = 0
        return size

# initialize Global variables 
def set_globvar(): 
    global GLOBAL_URL_QUEUE # queue
    GLOBAL_URL_QUEUE = []
    global GLOBAL_ALL_VISIT_QUEUE # queue
    GLOBAL_ALL_VISIT_QUEUE = []  
    global GLOBAL_MAXPAGE
    GLOBAL_MAXPAGE = 10 # initialize 10 pages 
    global GLOBAL_CUR_PAGE
    GLOBAL_CUR_PAGE = 0
    global COUNTER
    COUNTER = 0


    
   
   
# analyze the domain of URL
def getDomain(url):
    ret = urlparse.urlparse(url)
    if ret.hostname == None and ret.path != None:
        domain = ret.path.replace('/', '')
    else:
        domain = ret.hostname
    return domain

    
    
# get the link after domain
def getSubURL(url,domain):
    list = url.split(domain)
    if len(list)==1:
        return "/"
    else:
        return list[1]
 
 
# Read robot.txt, to understand the web can be fetched or not
class Robot:
    def __init__(self,url):
        try:
            self.url = url
            robotparser.URLopener.version = "Creole/0.1a" # for wiki [more info @ http://infix.se/2006/05/17/robotparser]
            self.rp = robotparser.RobotFileParser()
            self.rp.set_url( "http://"+getDomain(self.url)+"/robots.txt" )
            self.rp.read()
            print "http://"+getDomain(self.url)+"/robots.txt"
            self.err = True
        except StandardError,e:
            print "***** (Robot)connect StandardError(102) *****"
            print e
            self.err = False
            pass
            
    def robot_code(self,__url__):
        try:
            self.res = self.rp.can_fetch("*", __url__)
            print "robot_code="+str(self.rp.errcode) + " -> " + str(self.res)
            return self.res
        except StandardError,e:
            print "***** (Robot)connect StandardError(103) *****"
            print e
            return False
            
    def getErr(self):
        return self.err

 
# check the variables, for understand the content_type
def isset(v):  
    try:  
        type (v)  
    except:  
        return 0  
    else:  
        return 1          
        
        
# non-ASCII Encode
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)
    
# replace some character
def fix(x):
    p = re.compile(r'<[^<]*?>')
    return p.sub('', x).replace('&amp;', '&')

'''
### 抓取HTTP的內容
def getData(url):# 回傳抓到的HTML資料
    page = urllib.urlopen(url) # 存放http的資料
    return page.read() # return 讀取的資料    
'''
    
# defind the content-type we want( more info @ http://zh.wikipedia.org/zh-tw/MIME )
class Content_Type:
    def __init__(self):
        self.ctype = ['text/html']
    def getContentType(self):
        return self.ctype
    def check(self,url):
        try:
            url = urlEncodeNonAscii(url)
            domain = getDomain(url)
            subURL = getSubURL(url,domain)
            conn = httplib.HTTPConnection(domain)
            conn.request("GET", subURL )
            res = conn.getresponse()
            print res.status, res.reason
            #print res.getheaders()
            
            code = res.status  # (return code, like 200  404  403)
            # return code
            if code==500: return False
            if code==404: return False
            if code==403: return False
            
        except IOError,e:
            print "***** connect IOError(104) *****"
            print e
            print ""
            return False
        except UnicodeError,e:
            print "***** connect UnicodeError(105) *****"
            print e
            print ""
            return False     
        except httplib.HTTPException,e:
            print "***** connect InvalidURL(106) *****"
            print e
            print ""
            return False
        else:
            try:
                print res.getheaders()
                content_type = res.getheader('Content-Type') # GET Content-Type
                content_length = res.getheader('Content-Length') # GET Content-Type
                
                print content_type, content_length
                #res.read();
                if isset(content_type):
                    for c_type in self.ctype:
                        if c_type in content_type: return True
                else:
                    print "***** Error: Can't Found \"Content-Type\" *****";
            except StandardError,e:# if we cannot get content-type, will appera some meaasge
                print "***** connect StandardError(107) *****"
                print e
                pass
            return False
       
# get top 10 result from Yahoo       
class YahooSearch:
    def __init__(self, query, page=1):     
        self.query = query
        self.page = page
        self.url = "http://search.yahoo.com/search?p=%s&b=%s" %(urllib.quote(self.query), ((self.page - 1) * 10 + 1))
        print "=>"+self.url
        page = urllib.urlopen(self.url) # store http data
        self.content = page.read()      # read http data to string
        
    def getresults(self):
        self.results = []
        # p = re.compile(r'(href="(.*?)")')
        # m=p.search('<a href="live.net" link="go2">')
        for i in re.findall('<h3><a id="link-(.+?)" class="yschttl spt" href="(.+?)">(.+?)</a></h3></div><span class=url>(.+?)</span>', self.content):
            id = i[0]
            list = i[1].split("\"")
            
            title = fix(i[2])
            content = fix(i[2])
            url = fix(i[3])
            self.results.append(YahooResult(title, content, list[0])) #fix problem (when  keyword = kfos, the top10 resultt is not correct)
        return self.results
 
    def getnextpage(self):
        return YahooSearch(self.query, self.page+1)
 
    search_results = property(fget=getresults)
    nextpage = property(fget=getnextpage)

class YahooResult:
    def __init__(self,title,content,url):
        self.title = title
        self.content = content
        self.url = url
        
### Check if url is already FOUND in VISIT list
class CheckVisit:
    def __init__(self,visit_url,input_url):
        self.visit_url = visit_url
        self.input_url = input_url
    
    def check(self):
        for url in self.visit_url:
            #print "==cv== :",url,"  ",self.input_url
            if url==self.input_url:
                print "  ** Dependence ** \n"
                return False

        return True

# URL filter, can put the condition here
class URL_filter:
    def __init__(self,url):
        self.url = url
    def check(self):
        if "irc://"  in self.url: return True
        if "mailto:" in self.url: return True
        if "javascript:" in self.url: return True
        if (self.url.rfind(".jpg")==len(self.url)-len(".jpg") ): return True # 找URL最後是否為   *****.jpg
        if (self.url.rfind(".xml")==len(self.url)-len(".xml") ): return True # 找URL最後是否為   *****.xml
        if (self.url.rfind(".gif")==len(self.url)-len(".gif") ): return True # 找URL最後是否為   *****.gif
        if (self.url.rfind(".png")==len(self.url)-len(".png") ): return True # 找URL最後是否為   *****.png
        if (self.url.rfind(".ico")==len(self.url)-len(".ico") ): return True # 找URL最後是否為   *****.ico
        if (self.url.rfind(".css")==len(self.url)-len(".css") ): return True # 找URL最後是否為   *****.css
        if (self.url.rfind(".rss")==len(self.url)-len(".rss") ): return True # 找URL最後是否為   *****.rss
        if (self.url.rfind(".msi")==len(self.url)-len(".msi") ): return True # 找URL最後是否為   *****.msi
        if (self.url.rfind(".exe")==len(self.url)-len(".exe") ): return True # 找URL最後是否為   *****.exe
        if (self.url.rfind(".rar")==len(self.url)-len(".rar") ): return True # 找URL最後是否為   *****.rar
        if (self.url.rfind(".tgz")==len(self.url)-len(".tgz") ): return True # 找URL最後是否為   *****.tgz
        if (self.url.rfind(".pdf")==len(self.url)-len(".pdf") ): return True # 找URL最後是否為   *****.pdf
        
# rebuild URL
'''
class Rebuild_url:
    def __init__(self,base_url,url):
        self.url = url
        self.base_url = base_url
        self.header = ["http://","https://"]
        
    def build(self):
        for header in self.header:
            #print "check "+header+"..."+self.url
            if header in self.url :
                return self.url
            else:
                if "#"==self.url: # 其實這個可以放到 URL_filter, 因為多了"#" 和原本的html頁面試相同的
                    return self.base_url + "/" + self.url
                else:
                    self.url = "/"+self.url
                    self.url = self.url.replace("//","/")
                    return "http://"+getDomain(self.base_url) + self.url
        return self.base_url + self.url
'''       
        

#for crawl result
class CrawlResult3:
    def __init__(self, URL, MAX_PAGE , CUR_PAGE , ALL_VISIT , CT ):
        self.url = URL   # assgin value to self.url IN __init__ , "OR" IN other DEF
        self.max_page = MAX_PAGE # set max page number
        self.cur_page = CUR_PAGE
        self.visit_all = ALL_VISIT
        self.counter = CT
        
    def result(self):
        global GLOBAL_CUR_PAGE
        GLOBAL_CUR_PAGE = self.cur_page
        global GLOBAL_ALL_VISIT_QUEUE
        GLOBAL_ALL_VISIT_QUEUE = self.visit_all
        global COUNTER
        COUNTER = self.counter

        
        if GLOBAL_CUR_PAGE >= self.max_page:
            #print "Eooooch"
            pass
        else:
            try:# get TIMEOUT => IOError
                response = urllib.urlopen(self.url)
                soup = BeautifulSoup(response)

                for tag in soup.findAll('a', href=True):
                    if GLOBAL_CUR_PAGE >= self.max_page:
                        break
                    print "current_page : "+str(GLOBAL_CUR_PAGE)+" "+str(self.max_page)
                    
                    link = tag['href']
                    # filter URL
                    if URL_filter(link).check():
                        print "##### FILTER: "+link
                        continue
                    
                    # cut out srting form the link behind the symbol #
                    tmp = link.split("#")
                    link = tmp[0]
                    # rebuild LINK [urljoin]
                    link = urljoin(self.url,link)
                    #link = Rebuild_url(self.url,link).build()

                    cv = CheckVisit( GLOBAL_ALL_VISIT_QUEUE , link) # Queue
                    print "    "+link        
              
                    rb = Robot(link) # new Robot OBJ
                    if rb.getErr==False:    
                        pass
                    elif rb.robot_code(link) and cv.check() and Content_Type().check(link) : #if url is not Found && MIME type is correct ,then Append!
                        #print getData(link)
                        print 'ok\n'
                        GLOBAL_ALL_VISIT_QUEUE.append(link)
                        GLOBAL_URL_QUEUE.append( [ link , GLOBAL_URL_QUEUE[COUNTER][1]+1] )
                        tmp_size = http_download(link)
                        file_visit.write( str(GLOBAL_CUR_PAGE) + " Depth:"+str(GLOBAL_URL_QUEUE[COUNTER][1]+1)+"-"+str(COUNTER) + "\t" + link + "\t" + str(tmp_size) + "bytes" +"\n")
                        GLOBAL_CUR_PAGE += 1  
            except IOError,e:
                print "***** Error(110) *****", e
                
        COUNTER += 1
        if (COUNTER >= len(GLOBAL_URL_QUEUE) ):
            return

        cr3 = CrawlResult3( GLOBAL_URL_QUEUE[COUNTER][0], GLOBAL_MAXPAGE , GLOBAL_CUR_PAGE , GLOBAL_ALL_VISIT_QUEUE , COUNTER )
        cr3.result()
 
  
######## Main Start ########

starttime = time.clock() # execute time
socket.setdefaulttimeout(20) # timeout set 20 sec
set_globvar() # set Global variables 


# Usage:
pages = int(input("How many pages you want to crawl:  "))
print pages
GLOBAL_MAXPAGE = pages

query = raw_input("Input the keyword you want to search:  ")
print query

x = YahooSearch(query)

dir_path = os.getcwd() # find the current working directory
work_path = dir_path + r"\pages"
info_path = dir_path + r"\info"
if os.path.exists(work_path)==False: 
    os.makedirs(work_path)

if os.path.exists(info_path)==False: 
    os.makedirs(info_path)

file  = open( info_path + "/GLOBAL_URL_QUEUE.txt","w" ) # write data  
file_top10 = open( info_path + "/out_top10.txt","w") # TOP 10 results
file_visit = open( info_path + "/out_visit.txt","w") # ALL visit URLs


#alr_visit = []
for result in x.search_results:
    print result.url
    GLOBAL_ALL_VISIT_QUEUE.append( result.url ) #store TOP10 into ALL_VISIT queue
    file_top10.write(  result.title +"  ["+result.url+"]\n" )
    tmp_size = http_download(result.url)
    

for result in x.search_results:
    GLOBAL_CUR_PAGE = 0 # initialize
    GLOBAL_URL_QUEUE.append( [result.url , 0 ] ) # put TOP10 url,depth=0  into queue
    print result.title+"  ["+result.url+"]"
    file_visit.write(  result.title+"  ["+result.url+"]\n" )
    cr3 = CrawlResult3(result.url, GLOBAL_MAXPAGE , 0 , GLOBAL_ALL_VISIT_QUEUE , COUNTER)    # new a CrawlResult3 OBJECT
    cr3.result() 
    file_visit.write( "\n" )

# store GLOBAL_URL_QUEUE into txt file    
idx=0
for data in GLOBAL_URL_QUEUE:
    file.write(str(idx)+" :"+ str(data[1])+"\t"+data[0]+"\n" )
    idx += 1
    

#file.close()
#file_top10.close()
#file_visit.close()

endtime = time.clock()  
print "\n\nTime: " + str(endtime-starttime)
file_visit.write( "Time: "+str(endtime-starttime) + "\n" )

    
file.close()
file_top10.close()
file_visit.close()

#'''# END of main