import tkinter as tk
from tkinter import filedialog
import re
import os
import sys
import find_replace

current_file_path = None  # Initialize current_file_path as None

def new_file(event=None):
    global current_file_path
    text.delete(1.0, tk.END)  # Clear the current text widget
    root.title("Editor")  # Reset the window title
    current_file_path = None  # Reset the current file path


def delete_word_backwards(self):
    cursor_position = text.index("insert")

    # Find the end of the current word by searching for the next space character
    word_end = text.search(r"\S", cursor_position, backwards=True, regexp=True)
    word_end= text.index(f"{word_end}+1c") # Move word_end one character forward

    word_start = text.search(r"\s", f"{word_end}", backwards=True, regexp=True)

    if word_start==cursor_position:
        word_start= 0.0
       
    word_start= text.index(f"{word_start}+2c") # Move word_start one character forward

    text.delete(word_start, cursor_position)


def center_window(window):
    window_width = 1000
    window_height = 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

def open_file(event=None):
    global current_file_path
    file_path = filedialog.askopenfilename(parent=root, defaultextension=".txt")
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
        # Get the file name from the file path
        file_name = os.path.basename(file_path)
        root.title(f"{file_name} - Editor")
        current_file_path = file_path

def save_file(event=None):
    global current_file_path
    if current_file_path:
        with open(current_file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))
    else:
        save_as_file()  # If current_file_path is not defined, use "Save As"

def save_as_file():
    global current_file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))
        # Get the file name from the file path
        file_name = os.path.basename(file_path)
        root.title(f"{file_name} - Editor")
        current_file_path = file_path  # Update current_file_path

def capitalize_selected_text():
    # Get the selected text
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    if selected_text:
        # Capitalize the first letter of each word while preserving newlines
        capitalized_text = ""
        for line in selected_text.splitlines():
            words = line.split()
            capitalized_words = [word.capitalize() for word in words]
            capitalized_line = " ".join(capitalized_words)
            capitalized_text += capitalized_line + "\n"
        # Remove the trailing newline added above
        capitalized_text = capitalized_text.rstrip("\n")
        # Replace the selected text with the capitalized text
        text.replace(tk.SEL_FIRST, tk.SEL_LAST, capitalized_text)

def add_bullets():
    # Get the selected text
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    selected_text = capitalize_first_letter_of_each_line(selected_text)
    #selected_text = capitalize_first_letter_of_each_sentence(selected_text)

    # Add bullets to non-empty lines
    formatted_text = "\n".join(["- " + line if line.strip() != "" and not line.startswith("- ") else line for line in selected_text.split("\n")])
    # Replace the selected text with the formatted text
    text.replace(tk.SEL_FIRST, tk.SEL_LAST, formatted_text)

def add_tabs():
    # Get the selected text
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    
    # Add tabs to non-empty lines
    formatted_text = "\n".join(["\t" + line if line.strip() != "" else line for line in selected_text.split("\n")])
    # Replace the selected text with the formatted text
    text.replace(tk.SEL_FIRST, tk.SEL_LAST, formatted_text)


def capitalize_first_letter_of_each_line(selected_text):
    if selected_text:
        # Split the selected text into lines
        lines = selected_text.split('\n')
        # Capitalize the first letter of each line
        capitalized_lines = [line.capitalize() for line in lines]
        # Join the lines back together
        capitalized_text = '\n'.join(capitalized_lines)
        return capitalized_text


# Create the main window
root = tk.Tk()
root.title("Editor")

#def minimize_window():
#    root.iconify()  # Minimize the window
# Bind the minimize_window function to the WM_DELETE_WINDOW protocol
#root.protocol("WM_DELETE_WINDOW", minimize_window) # Minimize the window

# Make the window resizable
root.resizable(True, True)

# Center the window on the screen
center_window(root)

# Create a text widget with a fixed size
text = tk.Text(root, font=("Consolas", 11), width=1000, height=1000, wrap="word", undo=True, autoseparators=True, maxundo=-1)
text.pack()
text.focus()

# Create a menu bar
menu = tk.Menu(root)
root.config(menu=menu)

# File menu
file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")  # Add a "New" menu item
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Edit menu
edit_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Capitalize Every Word", command=capitalize_selected_text)
edit_menu.add_command(label="Insert Bullets", command=add_bullets)
edit_menu.add_command(label="Insert Tabs", command=add_tabs)
# edit_menu.add_separator()
# edit_menu.add_command(label="Find and Replace", command=lambda: find_replace.open_find_replace(root, text))


# Bind hotkeys
text.bind("<Control-n>", new_file)
text.bind("<Control-s>", save_file)
text.bind("<Control-o>", open_file)
text.bind("<Control-BackSpace>", delete_word_backwards)

# Create a toolbar
toolbar = tk.Frame(root)
toolbar.pack(fill="x")

# Add a button to capitalize selected text
capitalize_button = tk.Button(toolbar, text="Capitalize", command=capitalize_selected_text)
capitalize_button.pack(side="left")

# Run the main loop
root.mainloop()