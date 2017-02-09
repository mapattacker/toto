import sqlite3, urllib, json

# connect to database
conn = sqlite3.connect('toto.sqlite')
cur = conn.cursor()

googleapi='https://maps.googleapis.com/maps/api/geocode/json?address='
query=cur.execute('SELECT postal_code FROM placeall WHERE scanned=0').fetchall()


for i in query:
    for i in i:
        print i
        try:
            url=('{}{}').format(googleapi,i)
            html = urllib.urlopen(url).read()
            jsonP = json.loads(html)
            lat = jsonP['results'][0]['geometry']['location']['lat']
            long = jsonP['results'][0]['geometry']['location']['lng']
            cur.execute('UPDATE placeall SET latitude=?,longitude=?,scanned=? WHERE postal_code=?', (lat,long,1,i,))
            conn.commit()
        except:
            pass

print 'done'
