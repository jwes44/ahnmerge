import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('c:/Users/j/geonames.db')
    f = open('c:/Users/j/gec.txt')
    c = conn.cursor()
    i = 1
    for line in f:
        c.execute('DELETE FROM alternateNamesV2 WHERE geonameid=?', [line])
        i += 1
        if i > 1000:
            print('.',end='')
            i = 1
    conn.commit()
    conn.close()
    f.close()



