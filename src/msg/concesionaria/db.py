import sqlite3

def print_lines():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT desc_marca FROM cars limit 10")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()

if __name__ == "__main__":
    print_lines()
