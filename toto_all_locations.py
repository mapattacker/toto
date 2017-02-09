# get all locations where one can buy TOTO
import sqlite3, urllib
from selenium import webdriver
from bs4 import BeautifulSoup

# connect to database
conn = sqlite3.connect('toto.sqlite')
cur = conn.cursor()

url='http://www.singaporepools.com.sg/outlets/Pages/lo_results.aspx?sppl=cz0mej1BJm89QSZjPUEmZD1B'
html=urllib.urlopen(url).read()

soup = BeautifulSoup(html, 'html.parser')

for a in soup.select('table[id="tblOutletSearchResult"] li'):
    a= a.getText().replace(u'\xa0', u'').replace('  ',' ').split('\n')
    location = a[1].strip()
    address= a[2].strip()
    postal = re.search('Singapore\s\d+', address).group()
    cur.execute("INSERT OR IGNORE INTO placeall(location,address) VALUES(?,?)",(location,address,))

conn.commit()
conn.close()
print 'done'
