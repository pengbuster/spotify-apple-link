import sqlite3

connection = sqlite3.connect('keys_database.db')

cursor = connection.cursor()

cursor.executescript('''
    INSERT INTO test_table (user_id, authorization, access_code, refresh_code) 
    VALUES ('tettewg', 'poopoo', 'bruh', 'eoj');
''')

cursor.close()
connection.close()