import os
import sqlite3
import string
import sys
import re

if os.path.isfile('tf.db'):
    os.remove('tf.db')

with sqlite3.connect('tf.db') as connection:
    c = connection.cursor()
    c.execute('CREATE TABLE words (id INTEGER PRIMARY KEY AUTOINCREMENT, page INTEGER NOT NULL, value TEXT NOT NULL)')
    c.execute('CREATE TABLE targets (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT NOT NULL)')
    with open('../../target_words.txt') as f:
        for target_word in f.read().split(','):
            c.execute('INSERT INTO targets(value) VALUES (?)', (target_word, ))
    with open(sys.argv[1]) as f:
        for i, line in enumerate(f):
            for word in re.findall(r'\w+', line.lower()):
                c.execute('INSERT INTO words (page, value) VALUES (?, ?)', (i//45+1, word))

                    
    c.execute("""
        SELECT v1 || ' ' || v2 || ' ' || v3 || ' ' || v4 || ' ' || v5 || ' - ' || page
        FROM (
          SELECT 
            LAG(value, 2) OVER(ORDER BY id)  AS v1, 
            LAG(value, 1) OVER(ORDER BY id)  AS v2, 
            value                            AS v3,
            LEAD(value, 1) OVER(ORDER BY id) AS v4, 
            LEAD(value, 2) OVER(ORDER BY id) AS v5,
            page
          FROM words
        ) X
        WHERE EXISTS (SELECT * FROM targets W WHERE W.value = X.v3)
        ORDER BY v3
    """)
    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row[0])