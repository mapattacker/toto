from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3, platform, re

# connect to database
conn = sqlite3.connect('toto.sqlite')
cur = conn.cursor()

# connect to windows or mac chromedriver
if platform.system() == 'Windows':
    cdriver = r'C:\xxx\MyPythonScripts\chromedriver.exe'
else: # for macOS
    cdriver = r'/xxx/MyPythonScripts/chromedriver_mac'


url='http://www.singaporepools.com.sg/en/product/sr/Pages/toto_results.aspx?sppl=RHJhd051bWJlcj0zMjM4'
driver=webdriver.Chrome(cdriver)
driver.get(url)
html = driver.page_source.encode('utf-8')


# get list of toto draw numbers and put in database
alltoto = re.findall(r'value="(\d\d\d\d)',html)
for i in alltoto:
    cur.execute("INSERT OR IGNORE INTO date(draw_no) VALUES(?)",(i,))
conn.commit()

# extract draw numbers not scanned
cur.execute("SELECT draw_no FROM date WHERE scanned=0")
alltoto=cur.fetchall()


for i in alltoto:
    for i in i:
        string = "//select[@class='form-control selectDrawList']/option[@value='{}']".format(i)
        driver.find_element_by_xpath(string).click()

        # get new html
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # get date
        date=soup.select('th[class="drawDate"]')[0].getText().split(', ')
        day=date[0]
        date1=date[1]
        cur.execute("UPDATE date SET day=?,date=?,scanned=? WHERE draw_no=?", (day,date1,1,i,))
        print date

        # first 6 numbers
        text=soup.select('td[width="16%"]')
        y=0
        for ab in text:
            firstsix = ab.getText()
            y+=1
            if y == 5: pass
            cur.execute("INSERT OR IGNORE INTO jackpot_no(draw_no,no_type,number) VALUES(?,?,?)",(i,'normal',firstsix,))
        # additional number
        additional = soup.select('td[class="additional"]')[0].getText()
        cur.execute("INSERT OR IGNORE INTO jackpot_no(draw_no,no_type,number) VALUES(?,?,?)",(i,'additional',additional,))


        # get locations
        if html.find('Group 1 has no winner')>0:
            pass
        else:
            # cut html till group 1 winner only, ie. remove group 2 winners
            html = html[:html.find('Group 2 winning tickets')]
            soup = BeautifulSoup(html, 'html.parser')
            text=soup.select('li')
            try:
                for t in text:
                    a= t.getText().replace('\n','').replace('  ','').replace(' )','').split('( ')
                    b= t.getText()
                    location = a[0].split(' - ')
                    place = location[0]
                    address = location[1]
                    if a[1].find('QuickPick')==-1:
                        drawtype = re.search(r'1\s(\w+)\sE',a[1])
                        draw = 'No QuickPick'
                        system = drawtype.group(1)
                    else:
                        drawtype = re.search(r'1\s(\w+)\s(.+)\sE',a[1])
                        draw = drawtype.group(1)
                        system = drawtype.group(2)
                    print location
                    print draw
                    print system
                    cur.execute("INSERT OR IGNORE INTO place(draw_no,raw_data,location,address,quickpick,system) VALUES(?,?,?,?,?,?)",(i,b,place,address,draw,system,))
            except:
                pass
        conn.commit()
