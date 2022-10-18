"""
You must create a database for your program to use including at least one table to store data into.

Your software must demonstrate the ability to insert, modify, delete, and retrieve (or query) data.

This module requires more than just creating the database and determining SQL commands. 
You must write software that builds the SQL commands, submits them, receives the results from the database, and uses the results in some way.
"""

import sqlite3 as sql


def insertIntoTable(conn, cursor, valuesTuple):
    """
    Function for inserting values into a specified table using SQL commands
    """

    values = valuesTuple
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", values)
    conn.commit()


def viewTable(cursor):
    """
    Loops through each row and prints them to the terminal
    """
    for row in cursor.execute('SELECT * FROM users'):
        print(row)

def dropTable(cursor):
    """
    Completely deletes a table from the database.  This cannot be undone!!
    """
    cursor.execute("DROP TABLE IF EXISTS users")

def createTable(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS users
                    (name CHAR(25), email CHAR(50), phone CHAR(11))""")

def deleteRow(conn, cursor, name):
    values = (name,)
    cursor.execute("""DELETE FROM users
                    WHERE name=?

                    
                        """, values)

    conn.commit()
def main():
    conn = sql.connect("./practice.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (name, email, phone)''')

# Insert a row of data
    

    while True:
        print("Select an option")
        print("1. View table")
        print("2. Insert")
        print("3. Delete")
        print("4. Drop table")
        print("5. Create table")
        print("6. Quit")
        selection = input(" ")
        if selection == "6":
            break
        elif selection == "2":
            name = input("Enter a name: ")
            email = input("Enter an email: ")
            phone = input("Enter a phone number: ")
            insertIntoTable(conn, cursor, (name, email, phone))
        elif selection == "1":
            viewTable(cursor)
        elif selection == "4":
            dropTable(cursor)
        elif selection == "5":
            createTable(cursor)
        elif selection == "3":
            name = input("Who would you like to delete? ")
            deleteRow(conn, cursor, name)
    # cursor.execute("INSERT INTO users VALUES ('Seth Wilding','sawilding7@gmail.com','435-881-1384')")

    # Save (commit) the changes
    conn.commit()


    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

if __name__ == "__main__":
    main()