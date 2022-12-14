# Overview

This software was written to advance my understanding of SQL relational databases and using another programming language to create SQL commands.  

Software made using Python and and SQL database.  The database stores every book, chapter, verse, and verse text in the Book of Mormon.  The user can enter a verse in the input to be displayed.  The user can add or remove the verse in the input to a "favorites" table in the database to be viewed later.  The user can also display all of the scripture mastery verses in the Book of Mormon.

Here is a video walkthrough of the program.

[Software Demo Video](https://youtu.be/Ma-a4CR4SUU)

# Relational Database

The database used is a SQL relational database.  The SQL commands are created using Python SQLite3.

## Database Structure

### "Book of Mormon" Table
| book CHAR(30) | chapter CHAR(30) | verse CHAR(30) | text MEDIUMTEXT|
|--|--|--|--|
| 1 Nephi | 3 | 1 Nephi 3:7 | text of the verse |

### "favorites" Table
| verse CHAR(30) | text MEDIUMTEXT | date DATETIME |
|--|--|--|
| 1 Nephi 3:7 | text of the verse | date and time of insertion |

# Development Environment

* VS code
* Python
* SQLite3
* SQL database
* TKInter (GUI)


# Useful Websites

* [Python.org](https://docs.python.org/3/library/sqlite3.html)
* [SQLTutorial.net](https://www.sqlitetutorial.net/sqlite-python/)
* [TutorialsPoint.com](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)

# Future Work

* Make results scrollbar height dynamic based on the size of the results being displayed.
* Allow user to add multiple verses to their favorites using dash notation (1 Nephi 3:7-12).
* Improve layout of the GUI to be more intuitive.