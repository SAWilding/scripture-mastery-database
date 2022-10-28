import tkinter as tk
import datetime

# CONSTANTS
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500


scripture_mastery = ["1 Nephi 3:7",
                    "1 Nephi 19:23",
                    "2 Nephi 2:25",
                    "2 Nephi 2:27",
                    "2 Nephi 9:28-29",
                    "2 Nephi 28:7-9",
                    "2 Nephi 32:3",
                    "2 Nephi 32:8-9",
                    "Jacob 2:18-19",
                    "Mosiah 2:17",
                    "Mosiah 3:19",
                    "Mosiah 4:30",
                    "Alma 32:21",
                    "Alma 34:32-34",
                    "Alma 37:6-7",
                    "Alma 37:35",
                    "Alma 41:10",
                    "Helaman 5:12",
                    "3 Nephi 11:29",
                    "3 Nephi 27:27",
                    "Ether 12:6",
                    "Ether 12:27",
                    "Moroni 7:16-17",
                    "Moroni 7:45",
                    "Moroni 10:4-5"
                    ]

class App(tk.Frame):
    def __init__(self, master, cursor):
        super().__init__(master)
        self.cursor = cursor
        self.pack()
        self.create_sm_button()
        self.create_add_fs_button()
        self.create_remove_fs_button()
        self.create_display_fs_button()
        self.create_text_entry()
        self.create_canvas()

    def create_canvas(self):
        """
        Create canvas where the results will be displayed for each display function
        """
        
        frame=tk.Frame(self.master,width=WINDOW_WIDTH,height=WINDOW_HEIGHT)
        frame.pack(expand=True, fill=tk.BOTH)
        self.canvas=tk.Canvas(frame,width=WINDOW_WIDTH,height=WINDOW_HEIGHT,scrollregion=(0,0,WINDOW_WIDTH, 3000))

        vbar=tk.Scrollbar(frame,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)


    def create_text_entry(self):
        """
        Create a text input box to search for specific scripture references
        """
        self.reference = tk.Entry(width=50)
        self.reference.pack(side=tk.TOP)

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("1 Nephi 3:7")
        # Tell the entry widget to watch this variable.
        self.reference["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.reference.bind('<Key-Return>',
                             self.display_reference)

    def create_add_fs_button(self):
        """
        Create a button to add the current verse in the input to the favorite verses table in the database
        """
        self.fs_button = tk.Button(self.master, command=self.add_fs, text="Add to favorites")
        self.fs_button.pack(side=tk.TOP)

    def create_remove_fs_button(self):
        """
        Create a button to remove the current verse from the favorites table
        """
        self.fs_delete = tk.Button(self.master, command=self.delete_fs, text="Remove from favorites")
      
        self.fs_delete.pack()

    def create_display_fs_button(self):
        """
        Create button to display favorites
        """
        self.fs_display = tk.Button(self.master, command=self.display_fs, text="Show favorites")
        self.fs_display.pack(side=tk.TOP)
    def create_sm_button(self):
        """
        Create a button to display scripture mastery verses to the results canvas
        """
        self.sm_button = tk.Button(self.master, command=self.display_sm, text="Display Scripture Mastery Verses")
        self.sm_button.pack(side=tk.TOP)

    def display_reference(self, event):
        """
        Find and print a verse give by user input
        """
        # TODO allow function to print multiple verses "Moroni 10:4–5"
        reference = self.reference.get()
        if "-" in reference:
            text = self.display_multiple_verses(reference)
            self.canvas.delete("all")
            self.canvas.create_text(self.canvas.winfo_width() / 2, len(text) // 6, text=text, width=WINDOW_WIDTH - 25)

        else:
            try:
                values = (reference,)
                verse = self.cursor.execute("SELECT text FROM 'Book of Mormon' WHERE verse=?", values)
                self.canvas.delete("all")
                self.canvas.create_text(self.canvas.winfo_width() / 2, 50, text=f"{reference} - {verse.fetchone()[0]}", width=WINDOW_WIDTH - 25)
            except:
                self.canvas.delete("all")
                self.canvas.create_text(self.canvas.winfo_width() / 2, 50, text="Enter a scripture verse in this format: 1 Nephi 3:7", width=WINDOW_WIDTH - 25)
    
    def display_sm(self):
        """
        Function called when sm button is clicked to display scripture mastery verses in the canvas
        """

        self.canvas.delete("all")
        all_verses = ""
        for verse in scripture_mastery:
            if "-" in verse:
                all_verses += self.display_multiple_verses(verse)
            else:
                values = (verse,)
                sm_verse = self.cursor.execute("SELECT text FROM 'Book of Mormon' WHERE verse=?", values)
                all_verses += f"{verse} - {sm_verse.fetchone()[0]}\n"
        self.canvas.create_text(self.canvas.winfo_width() / 2, 1200, text=all_verses, width=WINDOW_WIDTH - 25)

    def add_fs(self):
        """
        Called when fs_button is clicked to add verse to favorites table
        """
        # Create favorites table if it does not alread exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS 'favorites'
            (verse CHAR(30), text MEDIUMTEXT, date DATETIME)''')

        # Add verse and text to the favorites table 
        fs_reference = self.reference.get()
        values = (fs_reference,)

        date_and_time = datetime.datetime.now()
        print(date_and_time)
        # try:
        fs_text = self.cursor.execute("SELECT text FROM 'Book of Mormon' WHERE verse=?", values).fetchone()[0]
        values = (fs_reference, fs_text, date_and_time)
        self.cursor.execute("INSERT INTO 'favorites' VALUES (?, ?, ?)", values)
        # except:
        #     print("Verse not found in database")

    def delete_fs(self):
        """
        Called when remove_fs_button is clicked to remove a verse from the favorites table
        """
        # Get the reference from the text input
        fs_reference = self.reference.get()
        values = (fs_reference,)
        try:
            self.cursor.execute("DELETE FROM 'favorites' WHERE verse=?", values)
        except:
            print("Verse not found in favorites table")

    def display_fs(self):
        """
        Called when fs_display is clicked to show the verses in the favorites table
        """
        # Clear the canvas
        self.canvas.delete("all")
        verses = self.cursor.execute("SELECT * FROM 'favorites' ORDER BY date DESC").fetchall()
        verses_text = ""
        for verse in verses:
            verses_text += f'{verse}\n'
        self.canvas.create_text(self.canvas.winfo_width() / 2, len(verses_text) // 5, text=verses_text, width=WINDOW_WIDTH - 25)
    
    def display_multiple_verses(self, reference):
        """
        Function to handle the display of multiple verses
        """
        # List for saving all references to display
        verses_to_display = []

        # split reference
        initial_reference = reference.split("-")[0]
        # End and start verse numbers as strings
        end_verse = reference.split("-")[1]
        start_verse = initial_reference.split(":")[1] 
 
        # Get book and chapter of initial reference to create references for other verses
        values = (initial_reference,)
        book = self.cursor.execute("SELECT book FROM 'Book of Mormon' WHERE verse=?", values).fetchone()[0]
        chapter = self.cursor.execute("SELECT chapter FROM 'Book of Mormon' WHERE verse=?", values).fetchone()[0]

        book_and_chapter = book + " " + chapter # 1 Nephi 3

        # Loop through verse numbers and create complete references for each and append to verses_to_display list
        for verse_number in range(int(start_verse), int(end_verse) + 1):
            complete_reference = book_and_chapter + ":" + str(verse_number) # 1 Nephi 3:7
            verses_to_display.append(complete_reference) 
        
        # Loop through each verse in verses_to_display and get their text and add it to text_to_display
        text_to_display = ""
        for verse in verses_to_display:
            values = (verse,)
            text_to_add = verse + " - " + self.cursor.execute("SELECT text FROM 'Book of Mormon' WHERE verse=?", values).fetchone()[0]
            text_to_display += text_to_add + "\n"

        return text_to_display

