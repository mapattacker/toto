import sqlite3

######### CREATE SQLITE TABLE ############
conn = sqlite3.connect('toto.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS date;
DROP TABLE IF EXISTS jackpot_no;
DROP TABLE IF EXISTS place;


CREATE TABLE date (
    draw_no         INTEGER UNIQUE,
    day             TEXT,
    date            TEXT UNIQUE,
    scanned         INTEGER DEFAULT 0
);

CREATE TABLE jackpot_no (
    draw_no         INTEGER,
    no_type         TEXT,
    number          INTEGER
);

CREATE TABLE place (
    draw_no         INTEGER,
    raw_data        TEXT,
    location        TEXT,
    address         TEXT,
    quickpick       TEXT,
    system          TEXT
);

CREATE TABLE placeall (
    location        TEXT,
    address         TEXT,
    latitude        FLOAT,
    longitude       FLOAT
    scanned         INTEGER DEFAULT 0
)
''')

print 'Database and tables Created'
