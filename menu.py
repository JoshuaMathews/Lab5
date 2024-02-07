"""
A menu - you need to add the database and fill in the functions.
"""
import sqlite3


db = "lab5.sqlite"
table = "ChainsawJuggle"

conn = sqlite3.connect(db)
conn.execute('CREATE TABLE IF NOT EXISTS ChainsawJuggle (name TEXT UNIQUE, country TEXT, catches INT)')
conn.close()

# TODO create database table OR set up Peewee model to create table

def main():
    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    conn = sqlite3.connect(db)
    for row in conn.execute('select * from ' + table):
        print(f'Name: {row[0]}')
        print(f'Country: {row[1]}')
        print(f'Catches: {row[2]}')

    conn.close()

def search_by_name():
    name = input("Name: ")
    conn = sqlite3.connect(db)
    entries = conn.execute(f'select * from {table} where Name = ?', (name,)).fetchone()
    conn.close()

    if name not in entries:
        print("Name not found!")
        return

    print(f'Name: {entries[0]}')
    print(f'Country: {entries[1]}')
    print(f'Catches: {entries[2]}')


def add_new_record():
    name = input("Name: ")
    country = input("Country: ")
    catches = int(input("Catches (as an integer): "))

    if does_entry_exist(name, country):
        print("Entry already exists!")
        return

    conn = sqlite3.connect(db)
    conn.execute(f'insert into {table} values (?, ?, ?)', (name, country, catches))
    conn.commit()
    conn.close()


def edit_existing_record():
    name = input("Name: ")
    country = input("Country: ")
    catches = int(input("Catches (as an integer): "))

    if not does_entry_exist(name, country):
        print("Unable to find record.")
        return

    conn = sqlite3.connect(db)
    cur = conn.execute(f'update {table} set Catches = ? WHERE Name = ? AND Country = ?', (catches, name, country))
    row_count = cur.rowcount
    conn.commit()
    conn.close()

    if row_count == 1:
        print(f"Successfully updated {name}")
    else:
        print(f"Was unable to update {name}.")


def delete_record():
    name = input("Name: ")
    country = input("Country: ")

    if not does_entry_exist(name, country):
        print("Unable to find record.")
        return

    conn = sqlite3.connect(db)
    cur = conn.execute(f'delete from {table} WHERE Name = ? AND Country = ?', (name, country))
    row_count = cur.rowcount
    conn.commit()
    conn.close()

    if row_count == 1:
        print(f"Successfully deleted {name}")
    else:
        print(f"Was unable to delete {name}.")

def does_entry_exist(name, country):
    conn = sqlite3.connect(db)
    cur = conn.execute(f"select * from {table} where Name = ? and Country = ?", (name, country))
    return cur.fetchone()


if __name__ == '__main__':
    main()