import sqlite3
from sqlite3 import Error
from os import environ

create_table = '''
    CREATE TABLE patterns(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name TEXT,
        pattern TEXT
    );

'''

insert_to_table = '''
    INSERT INTO patterns(rule_name, pattern)
    VALUES ('disaster', '.*Disaster.'),
            ('cpu', '.*CPU.*'),
            ('ora', '.*ORA-\d+.*');
'''

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        
        conn.execute(create_table)
        conn.commit()

        conn.execute(insert_to_table)
        conn.commit()
        #print(sqlite3.version)
    except Error as e:
        #print(e)
        pass
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    path = environ.get("db")
    create_connection(path)