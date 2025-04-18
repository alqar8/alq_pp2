import psycopg2
import csv
from tabulate import tabulate

def create_connection():
    try:
        conn = psycopg2.connect(host="localhost", dbname="lab10", user="postgres", password="Admin123", port=5432)
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        exit(1)

def back_to_menu():
    return input('Type "back" to return to the list of commands: ').lower() == 'back'

def insert_data_from_console(cur):
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")
    cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))

def insert_data_from_csv(cur):
    filepath = input("Enter a file path with proper extension: ")
    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))
    except Exception as e:
        print("Error reading CSV file:", e)

def delete_data(cur):
    phone = input('Type phone number you want to delete: ')
    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))

def update_data(cur):
    column = input('Type the column to update (name, surname, phone): ').lower()
    old_value = input(f'Enter the {column} to change: ')
    new_value = input(f'Enter the new {column}: ')
    cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, old_value))

def query_data(cur):
    column = input("Enter the column name for search (id, name, surname, phone): ").lower()
    value = input(f"Enter the {column} value: ")
    cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))

def display_all_data(cur):
    cur.execute("SELECT * from phonebook;")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def main():
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS phonebook (
                      user_id SERIAL PRIMARY KEY,
                      name VARCHAR(255) NOT NULL,
                      surname VARCHAR(255) NOT NULL, 
                      phone VARCHAR(255) NOT NULL
                    )""")

    while True:
        print("""
        List of commands:
        1. Type "i" or "I" to INSERT data to the table.
        2. Type "u" or "U" to UPDATE data in the table.
        3. Type "q" or "Q" to QUERY data in the table.
        4. Type "d" or "D" to DELETE data from the table.
        5. Type "f" or "F" to close the program.
        6. Type "s" or "S" to see all data in the table.
        """)

        command = input().lower()

        if command in ['i', 'insert']:
            method = input('Type "csv" or "con" to choose option between uploading csv file or typing from console: ').lower()
            if method == 'con':
                insert_data_from_console(cur)
            elif method == 'csv':
                insert_data_from_csv(cur)
            conn.commit()
            if not back_to_menu(): break

        elif command in ['d', 'delete']:
            delete_data(cur)
            conn.commit()
            if not back_to_menu(): break

        elif command in ['u', 'update']:
            update_data(cur)
            conn.commit()
            if not back_to_menu(): break

        elif command in ['q', 'query']:
            query_data(cur)
            if not back_to_menu(): break

        elif command in ['s', 'show']:
            display_all_data(cur)
            if not back_to_menu(): break

        elif command in ['f', 'finish']:
            break

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()