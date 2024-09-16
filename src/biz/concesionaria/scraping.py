import csv
import sqlite3
from pathlib import Path

def create_database():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            in_num TEXT,
            mtm_fmm TEXT,
            t TEXT,
            fab TEXT,
            marca TEXT,
            tipo TEXT,
            mod TEXT,
            desc_marca TEXT,
            desc_modelo TEXT,
            desc_tipo TEXT,
            km_0 TEXT,
            year_2023 TEXT,
            year_2022 TEXT,
            year_2021 TEXT,
            year_2020 TEXT,
            year_2019 TEXT,
            year_2018 TEXT,
            year_2017 TEXT,
            year_2016 TEXT,
            year_2015 TEXT,
            year_2014 TEXT,
            year_2013 TEXT,
            year_2012 TEXT,
            year_2011 TEXT,
            year_2010 TEXT,
            year_2009 TEXT,
            year_2008 TEXT,
            year_2007 TEXT,
            year_2006 TEXT,
            year_2005 TEXT,
            year_2004 TEXT,
            year_2003 TEXT,
            year_2002 TEXT,
            year_2001 TEXT,
            year_2000 TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def insert_data(cursor, row):
    cursor.execute('''
        INSERT INTO cars (
            in_num, mtm_fmm, t, fab, marca, tipo, mod, desc_marca, desc_modelo, desc_tipo,
            km_0, year_2023, year_2022, year_2021, year_2020, year_2019, year_2018, year_2017,
            year_2016, year_2015, year_2014, year_2013, year_2012, year_2011, year_2010,
            year_2009, year_2008, year_2007, year_2006, year_2005, year_2004, year_2003,
            year_2002, year_2001, year_2000
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', row)

def read_csv_and_insert_to_db():
    conn, cursor = create_database()
    
    csv_file = Path(__file__).parent / 'dnrpa.csv'
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)
        
        for row in csv_reader:
            insert_data(cursor, row)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    read_csv_and_insert_to_db()
    print("Data has been successfully inserted into the database.")
