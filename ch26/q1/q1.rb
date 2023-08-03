require 'sqlite3'

def create_db_schema(db)
  db.execute('CREATE TABLE documents (id INTEGER PRIMARY KEY AUTOINCREMENT, name)')
  db.execute('CREATE TABLE words (id, doc_id, value)')
  db.execute('CREATE TABLE characters (id, word_id, value)')
end

def load_file_into_database(db, path_to_file)
  db.transaction do
    words = extract_words(path_to_file)
    db.execute('INSERT INTO documents (name) VALUES (?)', path_to_file)
    
    doc_id = db.execute('SELECT id from documents WHERE name=?', path_to_file)[0][0]

    word_id = nil
    db.execute('SELECT MAX(id) FROM words'){|row| doc_id = row[0]}
    word_id = 0 if word_id.nil?

    words.each do |w|
      db.execute('INSERT INTO words VALUES (?, ?, ?)', word_id, doc_id, w)
      char_id = 0
      w.chars.each do |char|
        db.execute('INSERT INTO characters VALUES (?, ?, ?)', char_id, word_id, char)
        char_id += 1
      end
      word_id += 1
    end
  end
end

def extract_words(path_to_file)
  word_list = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase.split
  stop_words = IO.read('../../stop_words.txt').split(',')
  stop_words.concat(('a'..'z').to_a)
  word_list.reject{|w| stop_words.include?(w)}
end


unless File.exist?('tf.db')
  SQLite3::Database.new('tf.db') do |db|
    create_db_schema(db)
    load_file_into_database(db, ARGV[0])
  end
end

SQLite3::Database.new('tf.db') do |db|
  x = 0
  db.execute('SELECT value, COUNT(*) as C FROM words GROUP BY value ORDER BY C DESC') do |row|
    break if x==25
    puts "#{row[0]} - #{row[1]}"
    x += 1
  end
end