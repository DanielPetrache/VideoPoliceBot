import sqlite3

conn = sqlite3.connect('emojis.db')

c = conn.cursor()

print(c.execute("PRAGMA foreign_keys;"))

tables_creation = ['''CREATE TABLE IF NOT EXISTS users(
                  id TEXT PRIMARY KEY NOT NULL ,
                  user_name TEXT NOT NULL
                  );''',
                  
                  '''CREATE TABLE IF NOT EXISTS emojis(
                  id TEXT PRIMARY KEY NOT NULL,
                  emoji_name TEXT NOT NULL
                  );''',
                  
                  '''CREATE TABLE IF NOT EXISTS emoji_count(
                  user_id TEXT NOT NULL,
                  emoji_id TEXT NOT NULL,
                  user_name TEXT NOT NULL,
                  emoji_name TEXT NOT NULL,
                  counter INTEGER NOT NULL,
                  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                  FOREIGN KEY(emoji_id) REFERENCES emojis(id) ON DELETE CASCADE
                  PRIMARY KEY (user_id, emoji_id)
                  );''']
                  

                  
for x in tables_creation:
    c.execute(x)

conn.commit()
conn.close()
