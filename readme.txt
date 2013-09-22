The program is for crawling website.
------------------------------------------------------------------------------------------------------------------

Compile:

using Python 2.7

put all the files in the same directory, there are 5 program files, BeautifulSoup.py , BeautifulSoup.pyc , 
BeautifulSoupTests.py , setup.py and main program tseng1.py

use command line to execute the program

>> python tseng1.py

and then input the N pages and Key words for crawling.

------------------------------------------------------------------------------------------------------------------

After executing the program, there are 3 txt files and 2 directory are generated

"out_top10.txt"		store the top10 search result from yahoo

"out_visit.txt"		store the web we crawl from every top10 result, depth, the distance from their parent ,and size 

"GLOBAL_URL_QUEUE.txt"	store all of the web we crawl

info			store three txt files

pages			store all html files we download

------------------------------------------------------------------------------------------------------------------

How to read txt files

"out_top10.txt"
just show top10 URL from yahoo search result


"out_visit.txt"
Keywords: "apple iphone"

Apple - iPhone 4 - Video calls, multitasking, HD video, and more  [http://www.apple.com/iphone/]
0 Depth:1-0	http://www.apple.com/mac/	23684kbs
1 Depth:1-0	http://www.apple.com/ipod/	17665kbs

18 Depth:2-22	http://www.apple.com/itunes/what-is/	19600kbs
19 Depth:2-22	http://www.apple.com/itunes/whats-on/	24111kbs


first number presents the page number we crawl from top10 result.
for example, 0 means it is the first page we find from the top10 result

Depth:2-22
2 means that it is in the second level. I assume that top10 result are in 0 level
22 means its parent is the 22 web in the GLOBAL_URL_QUEUE


"GLOBAL_URL_QUEUE.txt"
0 :0	http://www.apple.com/iphone/
1 :1	http://www.apple.com/mac/
2 :1	http://www.apple.com/ipod/
3 :1	http://www.apple.com/ipad/
4 :1	http://www.apple.com/itunes/
5 :1	http://www.apple.com/support/
6 :1	http://www.apple.com/iphone/features/
7 :1	http://www.apple.com/iphone/design

first number present the web's index
second number present the web's depth

------------------------------------------------------------------------------------------------------------------

