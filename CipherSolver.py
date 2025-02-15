""" LIBS: PERFORMANCE"""
import re
from functools import partial

""" LIB: GUI """
import tkinter as tk
from tkinter import *
from tkinter import messagebox 

class CipherSolver:
    """ CIPHER MECHANICS """

    def __init__(self,
        GIVEN_TEXT = '',
        TITLE = '',
        ALPHABET = 'abcdefghijklmnopqrstuvwxyz',
        USED_FONT = "Consolas",
        TEXT_COLOUR = "red",
        TEXT_SIZE = 20,
        TEXT_HEIGHT = 20,
        LABEL_SIZE = 20,
        DECIPHERED_COLOR = "green",
        ):

        """ SETTING CONSTANT ATTRIBUTES """
        self.GIVEN_TEXT = GIVEN_TEXT
        self.TITLE = TITLE
        self.ALPHABET = ALPHABET
        self.USED_FONT = USED_FONT
        self.TEXT_COLOUR = TEXT_COLOUR
        self.TEXT_SIZE = TEXT_SIZE
        self.TEXT_HEIGHT = TEXT_HEIGHT
        self.LABEL_SIZE = LABEL_SIZE
        self.DECIPHERED_COLOR = DECIPHERED_COLOR

        """ CREATING WINDOW """

        # creates the root window
        self.root = tk.Tk()

        # sets window title
        self.root.title(self.TITLE)

        # sets window size
        #self.root.geometry("700x500")

        """ ADDING ELEMENTS """
        self.origtxt = GIVEN_TEXT
        self.inputtxt = Text(self.root,
                        font = (self.USED_FONT, self.TEXT_SIZE),
                        fg=self.TEXT_COLOUR, height=self.TEXT_HEIGHT,
                        wrap=tk.WORD)
        self.replace_text(GIVEN_TEXT)
        self.inputtxt.config(state="disabled") # no more edits
        text = self.get_text()
        self.deciphered = self.get_basic_deciphered(text)
        self.replaced_counter = Label(text = "", font = (self.USED_FONT, self.LABEL_SIZE))

        self.replacements = {x:None for x in self.ALPHABET}

        self.inputtxt.pack()
        self.replaced_counter.pack()

        # Table of ALPHABET replacements
        columns = 6
        rows = int(len(self.ALPHABET) / columns) + 1
        self.create_table(rows, columns)

        """ ADDING TAGS """
        self.inputtxt.tag_config("black", foreground="black")
        self.inputtxt.tag_config("red", foreground="red")
        self.inputtxt.tag_config("green", foreground="green")
        self.inputtxt.tag_config("blue", foreground="blue")
        self.inputtxt.tag_config("purple", foreground="purple")
        self.inputtxt.tag_config("bold", font=(self.USED_FONT, self.TEXT_SIZE, "bold"), background="yellow")
    

    def is_letter(self, letter):
        return letter.lower() in self.ALPHABET

    def get_next_letter_id(self, from_id, text):
        if from_id == -1:
            return -1
        for i in range(from_id, len(text)):
            if is_letter(text[i]):
                return i
        return -1

    """ CALLBACKS """

    # Counts words in the text
    def count_words(self, text):
        return len(re.findall(r'\w+', text))

    # Updates word counter in GUI
    def update_word_counter(self):
        text = self.get_text()
        self.word_counter.config(text = f'Слов: {self.count_words(text)}')

    # Makes text basic font (colour, weight, ...)
    def recolour(self):
        for tag in self.inputtxt.tag_names():
            self.inputtxt.tag_remove(tag, "1.0", "end")

    # Replaces current shown text with 'new_text'
    def replace_text(self, new_text):
        self.inputtxt.delete("1.0", "end-1c")
        self.inputtxt.insert("end-1c", new_text)

    # Returns a list of [False, False, ...] the length of 'text'
    def get_basic_deciphered(self, text):
        return [False] * len(text)

    # Colours a letter by position 'i' as deciphered
    def colour_deciphered(self, i):
        self.inputtxt.tag_add(self.DECIPHERED_COLOR, f"1.0+{i}c", f"1.0+{i+1}c")

    def colour_undeciphered(self, i):
        self.inputtxt.tag_remove(self.DECIPHERED_COLOR, f"1.0+{i}c", f"1.0+{i+1}c")

    def get_text(self):
        return self.inputtxt.get('1.0', 'end-1c')

    def replace_letter(self, i, y):
        self.inputtxt.configure(state="normal")
        index = f"1.0 + {i}c"
        self.inputtxt.delete(index)
        self.inputtxt.insert(index, y)
        self.inputtxt.configure(state="disabled")

    def are_same(self, a, b):
        return a.lower() == b.lower()


    def is_letter(self, a):
        #return len(a) == 1 and a in self.ALPHABET

        # Here, we let the user change
        ## the letters into any other characters
        return len(a) == 1

    # Replaces all NON-DECIPHERED letters X -> Y
    def replace_all_letters(self, x, y):
        counter = 0
        if self.replacements[x]:
            messagebox.showerror("showerror", f"Буква {x} уже заменена!") 
            return
        text = self.get_text()
        for i in range(len(text)):
            if self.are_same(text[i], x) and not self.deciphered[i]:
                yy = y
                if text[i] != text[i].lower():
                    yy = y.upper()
                self.replace_letter(i, yy)
                self.deciphered[i] = True
                self.colour_deciphered(i)
                counter += 1
        self.replacements[x] = y
        return counter

    def delete_replacement(self, x, y):
        text = self.get_text()
        for i in range(len(text)):
            if self.are_same(text[i], y) and self.are_same(self.origtxt[i], x) and self.deciphered[i]:
                self.replace_letter(i, self.origtxt[i])
                self.deciphered[i] = False
                self.colour_undeciphered(i)
        self.replacements[x] = None

    def send_replacement(self):
        x = self.entry_x.get().lower()
        y = self.entry_y.get().lower()
        if self.is_letter(x) and self.is_letter(y):
            self.replace_all_letters(x, y)
        else:
            messagebox.showerror("showerror", "Заменить можно только букву на букву!") 

    # Inflects the Russian word 'раз'
    def get_raz(self, num):
        if num % 10 > 1 and num % 10 < 5:
            return 'раза'
        return 'раз'

    def replace_callback(self, entry, x, event):
        y = entry.get()
        if self.replacements[x]:
            self.delete_replacement(x, self.replacements[x])
        if y:
            y = y.lower()
            if self.is_letter(x) and self.is_letter(y):
                counter = self.replace_all_letters(x, y)
                self.replaced_counter.config(text = f"Заменено {counter} {self.get_raz(counter)}.")
            else:
                messagebox.showerror("showerror", "Заменить можно только букву на букву!")


    def create_table(self, rows, columns):
        # Create a frame for the table
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(padx=10, pady=10)
        
        # Store the label-entry widgets in a list for easy access
        self.letters = []
        
        # Create the table
        for row in range(rows):
            row_entries = []
            for col in range(columns):
                try:
                    cur_letter = self.ALPHABET[row * columns + col]
                except Exception as e:
                    break
                # Create the label
                label = tk.Label(self.table_frame, text=f"{cur_letter} → ", width=10, anchor="e", font=(self.USED_FONT, self.TEXT_SIZE))
                label.grid(row=row, column=col * 2, padx=5, pady=5, sticky="e")  # Place label in column 2 * col
                
                # Create the entry next to the label
                entry = tk.Entry(self.table_frame, width=2, justify="center", font=(self.USED_FONT, self.TEXT_SIZE))
                entry.bind('<KeyRelease>', partial(self.replace_callback, entry, cur_letter))
                entry.focus()
                entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)  # Place entry in column 2 * col + 1
                
                row_entries.append((label, entry))
            self.letters.append(row_entries)
        
        return self.letters

    def main(self):
        """ RUNNING THE WINDOW """

        # keeps the window running
        self.root.mainloop()
