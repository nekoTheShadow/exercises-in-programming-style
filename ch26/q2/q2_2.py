import sqlite3

with sqlite3.connect('tf.db') as connection:
    c = connection.cursor()
    c.execute('SELECT value, COUNT(*) as C FROM words GROUP BY value ORDER BY C DESC')
    for i in range(25):
        row = c.fetchone()
        if row != None:
            print(row[0], '-', str(row[1]))