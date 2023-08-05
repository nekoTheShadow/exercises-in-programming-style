import sys, re, string, sqlite3, os.path

def create_db_schema(connection):
    c = connection.cursor()
    c.execute('CREATE TABLE documents (id INTEGER PRIMARY KEY AUTOINCREMENT, name)')
    c.execute('CREATE TABLE words (id, doc_id, value)')
    c.execute('CREATE TABLE characters (id, word_id, value)')
    connection.commit()
    c.close()

def load_file_into_database(path_to_file, connection):
    def _extract_words(path_to_file):
        with open(path_to_file) as f:
            str_data = f.read()    
        pattern = re.compile('[\W_]+')
        word_list = pattern.sub(' ', str_data).lower().split()
        with open('../../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    words = _extract_words(path_to_file)

    c = connection.cursor()
    c.execute('INSERT INTO documents (name) VALUES (?)', (path_to_file,))
    c.execute('SELECT id from documents WHERE name=?', (path_to_file,))
    doc_id = c.fetchone()[0]

    c.execute('SELECT MAX(id) FROM words')
    row = c.fetchone()
    word_id = row[0]
    if word_id == None:
        word_id = 0
    else:
        word_id += 1
    for w in words:
        c.execute('INSERT INTO words VALUES (?, ?, ?)', (word_id, doc_id, w))
        char_id = 0
        for char in w:
            c.execute('INSERT INTO characters VALUES (?, ?, ?)', (char_id, word_id, char))
            char_id += 1
        word_id += 1
    connection.commit()
    c.close()

def load_files_into_database(path_to_files, connection):
        for path_to_file in path_to_files:
            load_file_into_database(path_to_file, connection)

def execute_query(c, title, query):
    print(title)
    c.execute(query)
    for row in c.fetchall():
        print(", ".join(f"{key}={row[key]}" for key in row.keys()))


if not os.path.isfile('tf.db'):
    with sqlite3.connect('tf.db') as connection:
        create_db_schema(connection)
        load_files_into_database(sys.argv[1:], connection)

with sqlite3.connect('tf.db') as connection:
    c = connection.cursor()
    c.row_factory = sqlite3.Row
    execute_query(c, "a.各書籍の頻出上位25単語", """
        SELECT D.name, Y.value, Y.c
        FROM (
          SELECT doc_id, value, c, ROW_NUMBER() OVER (PARTITION BY doc_id ORDER BY c DESC) AS r
          FROM (
            SELECT doc_id, value, COUNT(*) AS c
            FROM words W 
            GROUP BY doc_id, value
          ) AS X
        ) AS Y
        JOIN documents D ON Y.doc_id = D.id
        WHERE r <= 25
    """)
    execute_query(c, "b.各書籍の総単語数", "SELECT D.name, COUNT(*) AS c FROM words W JOIN documents D ON W.doc_id = D.id GROUP BY doc_id")
    execute_query(c, "c.各書籍の総文字数", """
        SELECT D.name, COUNT(*) AS c
        FROM documents D
        JOIN words W ON D.id = W.doc_id
        JOIN characters C ON W.id = C.word_id
        GROUP BY D.id
    """)
    execute_query(c, "d.各書籍の最も長い単語", """
        SELECT *
        FROM (
          SELECT D.name, W.value,  RANK() OVER (PARTITION BY D.id ORDER BY length(W.value) DESC) AS r
          FROM documents D
          JOIN words W ON D.id = W.doc_id
        ) X
        WHERE r = 1
    """)
    execute_query(c, "e.単語あたりの平均文字数", """
        SELECT D.name, AVG(length(W.value))
        FROM documents D
        JOIN words W ON D.id = W.doc_id
        GROUP BY D.id
    """)
    execute_query(c, "f.書籍の上位25語の文字長合計", """
        SELECT D.name, SUM(length(value))
        FROM (
          SELECT doc_id, value, c, ROW_NUMBER() OVER (PARTITION BY doc_id ORDER BY c DESC) AS r
          FROM (
            SELECT doc_id, value, COUNT(*) AS c
            FROM words W 
            GROUP BY doc_id, value
          ) AS X
        ) AS Y
        JOIN documents D ON Y.doc_id = D.id
        WHERE r <= 25
        GROUP BY doc_id
        
    """)