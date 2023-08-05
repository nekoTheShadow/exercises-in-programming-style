import os
import sqlite3
import string
import sys
import re

if os.path.isfile('tf.db'):
    os.remove('tf.db')

with open('../../stop_words.txt') as f:
    stop_words = f.read().split(',')
stop_words.extend(list(string.ascii_lowercase))

with sqlite3.connect('tf.db') as connection:
    c = connection.cursor()
    c.execute('CREATE TABLE words (id INTEGER PRIMARY KEY AUTOINCREMENT, page INTEGER NOT NULL, value TEXT NOT NULL)')
    with open(sys.argv[1]) as f:
        for i, line in enumerate(f):
            for word in re.findall(r'[a-z]+', line.lower()):
                if word not in stop_words:
                    c.execute('INSERT INTO words (page, value) VALUES (?, ?)', (i//45+1, word))
                
    c.execute("""
        SELECT value, GROUP_CONCAT(page, ',') AS pages 
        FROM (SELECT value, page, ROW_NUMBER() OVER (PARTITION BY value, page ORDER BY id) rn FROM words) X
        WHERE rn = 1
        GROUP BY value
        HAVING COUNT(*) < 100
        ORDER BY value
    """)
    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row[0], '-', ', '.join(map(str, map(int, row[1].split(',')))))