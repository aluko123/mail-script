import sqlite3
import csv

#creating a new SQLite database (or connect to an existing one)
connection = sqlite3.connect('email_mapping.db')


#create cursor object to execute SQL command
cursor = connection.cursor()


#define SQL to create table
create_table_sql = '''
CREATE TABLE IF NOT EXISTS email_mapping(
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL
);
'''

#execute SQL cursor to create table
cursor.execute(create_table_sql)

#specify csv path
file_path = 'email-phone.csv'

#read csv file to populate database
with open(file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    #skip header row
    next(csv_reader, None)

    #iterate through
    for row in csv_reader:
        email, phone_number = row
        
        #check if record already exists
        check_query = "SELECT * FROM email_mapping WHERE email = ?"
        cursor.execute(check_query, (email,))
        if cursor.fetchone() is None:
            insert_sql = 'INSERT INTO email_mapping (email, phone_number) VALUES (?, ?)'
            cursor.execute(insert_sql, (email, phone_number))


#commit changes and close db connection
connection.commit()
connection.close()