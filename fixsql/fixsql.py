import sqlite3
if __name__ == '__main__':
    insertsql = """INSERT INTO addresses(full_address,city,county,state,country,latitude,longitude) VALUES(?, ?, ?, ?, ?, ?, ?)"""
    conn = sqlite3.connect('c:/Users/j/ahnaddr2.db')
    conn.execute("CREATE TABLE IF NOT EXISTS addresses (adr_id INTEGER PRIMARY KEY, full_address STRING, city STRING, county STRING, state STRING, country STRING, latitude REAL, longitude REAL)")
    conn.execute("CREATE TABLE IF NOT EXISTS test_addresses (address STRING PRIMARY KEY NOT NULL, adr INTEGER REFERENCES addresses (adr_id)) WITHOUT ROWID")
    c = conn.cursor()
    # Create a secondary key on the name column
    createSecondaryIndex = "CREATE INDEX IF NOT EXISTS index_addresses ON addresses(full_address)"
    c.execute(createSecondaryIndex)

    conn1 = sqlite3.connect('file:c:/Users/j/ahnaddr1.db?mode=ro', uri=True)
    c1 = conn1.cursor()
    c1.execute('SELECT address, adr, full_address, city, county, state, country, latitude, longitude FROM test_addresses,addresses WHERE test_addresses.adr = addresses.adr_id')
    c1.row_factory = sqlite3.Row

    rows = c1.fetchall()
    for address in rows:
        c.execute('SELECT adr_id FROM addresses WHERE addresses.full_address = ?', (address['full_address'],))
        r = c.fetchone()
        if r:
            key = r[0]
        else:
            c.execute(insertsql, (address['full_address'],address['city'],address['county'],address['state'],address['country'],address['latitude'],address['longitude']) )
            key = c.lastrowid
        c.execute("INSERT INTO test_addresses VALUES (?,?)", (address['address'], key))

    conn.commit()
    conn.close()

