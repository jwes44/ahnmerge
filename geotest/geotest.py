import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('c:/Users/j/geonames.db')
#    f = open('c:/Users/j/geoerr.txt', 'w', encoding='utf-8')
    c = conn.cursor()
    c.execute('SELECT * FROM alternateNamesV2')
    ret = c.fetchall()
    for item in range(len(ret)):
        c.execute('SELECT * FROM geo WHERE geonameid=?', [ret[item][1]])
        if not c.fetchone():
#            print(ret[item], file=f)
            print(ret[item])
    conn.close()
#    f.close()


