import sqlite3
conn = sqlite3.connect('database.db')
print("BD otwarta")
conn.execute('CREATE TABLE posty (id INTEGER PRIMARY KEY, tytul TEXT, tresc TEXT, autor TEXT, usuniety INTEGER DEFAULT 0)')

#conn.execute('ALTER TABLE posty ADD usuniety INT')

print("Tabela utworzona")
conn.close()
