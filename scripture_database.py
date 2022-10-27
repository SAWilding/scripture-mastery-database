"""
You must create a database for your program to use including at least one table to store data into.

Your software must demonstrate the ability to insert, modify, delete, and retrieve (or query) data.

This module requires more than just creating the database and determining SQL commands. 
You must write software that builds the SQL commands, submits them, receives the results from the database, and uses the results in some way.
"""

import sqlite3 as sql
import json
import App 
import tkinter as tk

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500


def create_BOM_table(conn, cursor):

    """
    Loops through all of the verses in the BOM and adds them to the Book of Mormon table in the scripture_database.db file
    """
    # Open file and load with json package
    f = open("./bom.json") 
    bom = json.load(f)

    # Drop the table and restart
    cursor.execute("DROP TABLE IF EXISTS 'Book of Mormon'")


    # Recreate Book of Mormon Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS 'Book of Mormon'
            (book CHAR(30), chapter CHAR(30), verse CHAR(30), text MEDIUMTEXT)''')

    # Get references for book, chapter, verse, and text of verse
    # Most efficient??
    
    for book in bom["books"]:
        book_value = book["book"]

        for chapter in book["chapters"]:

            chapter_value = chapter["chapter"]

            for verse in chapter["verses"]:
                verse_value = verse["reference"]
                text = verse["text"]

            # Insert values into the database
                values = (book_value, chapter_value, verse_value, text)
                cursor.execute("INSERT INTO 'Book of Mormon' VALUES (?, ?, ?, ?)", values)

    # Commit changes
    conn.commit()

    # Close file 
    f.close()


def print_verse(cursor, reference):
    """
    Find and print a verse give by user input
    """
    # TODO allow function to print multiple verses "Moroni 10:4–5"
    values = (reference,)
    verse = cursor.execute("SELECT text FROM 'Book of Mormon' WHERE verse=?", values)

    print(f"{reference} - {verse.fetchone()[0]}")

    
def viewTable(cursor):
    """
    Loops through each row and prints them to the terminal
    """

    for row in cursor.execute("SELECT * FROM 'favorites'"):
        print(row)


def main():
    # Create connection with db
    conn = sql.connect("./scripture_database.db")
    cursor = conn.cursor()




    # Check is Book of Mormon table exists
    listOfTables = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='Book of Mormon'; """).fetchall()

    if listOfTables == []:
        print("Created new BOM table")
        create_BOM_table(conn, cursor)
    else:
        print("BOM table already exists")

    # print scripture mastery verses
    # for verse in scripture_mastery:
    #     print_verse(cursor, verse)

    # Create tkinter window
    root = tk.Tk()
    myapp = App.App(root, cursor)
    myapp.master.title("Scripture Database")
    myapp.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    myapp.mainloop()
    # Save changes and close the connection

    conn.commit()

    conn.close()



if __name__ == "__main__":
    main()





