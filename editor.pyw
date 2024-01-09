 
import tkinter as tk
from tkinter import filedialog, simpledialog
import re
import os
import sys
from tkinterdnd2 import DND_FILES, TkinterDnD
import ctypes
from tkinter import messagebox


current_file_path = None  # Initialize current_file_path as None

def find_replace_in_selection():
    # Get the current selection range
    sel_start = text.index(tk.SEL_FIRST)
    sel_end = text.index(tk.SEL_LAST + "+1c")  # Add "+1c" to include the last character

    # Get the selected text
    selected_text = text.get(sel_start, sel_end)

    # Show a dialog to get the find and replace strings
    find_str = simpledialog.askstring("Find and Replace", "Find:")
    replace_str = simpledialog.askstring("Find and Replace", "Replace with:")
    
    # Create a regular expression with the re.IGNORECASE flag
    pattern = re.compile(re.escape(find_str), re.IGNORECASE)

    # Perform find and replace in the selected text
    modified_text = pattern.sub(replace_str, selected_text)

    # Replace the selected text with the modified text
    text.replace(sel_start, sel_end, modified_text)


def prepend_lines_with_input():
    # Create a simple input dialog
    user_input = tk.simpledialog.askstring("Input", "Enter text to prepend to selected lines:")
    if user_input is not None:  # Check if the user entered something
        # Get the selected text
        selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            # Split the selected text into lines
            lines = selected_text.split('\n')
            # Prepend the user input to each line
            modified_lines = [user_input + line if line.strip() != '' else line for line in lines]
            # Join the modified lines back together
            modified_text = '\n'.join(modified_lines)
            # Replace the selected text with the modified text
            text.replace(tk.SEL_FIRST, tk.SEL_LAST, modified_text)

def is_read_only():
    file_path = current_file_path

    # Call the GetFileAttributesW function
    file_attributes = ctypes.windll.kernel32.GetFileAttributesW(file_path)

    x = 0

    # Check if the file is read-only
    if file_attributes != -1:  # -1 indicates an error
        is_read_only = file_attributes & 1  # Check the lowest bit (read-only bit)
        if is_read_only:
            # print(f"The file '{file_path}' is read-only.")
            return True
        else:
            # print(f"The file '{file_path}' is normal.")
            return False
    else:
        print(f"Failed to retrieve attributes for '{file_path}'.")

def set_attribute_readonly():
    file_path = current_file_path

    # Use the SetFileAttributesW function to set the read-only attribute
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 1)  # 1 corresponds to FILE_ATTRIBUTE_READONLY

    # Add read only tag to title
    new_text = " - [READ-ONLY]"
    current_title = root.title()
    updated_title = current_title + new_text
    root.title(updated_title)

def set_attribute_normal():

    file_path = current_file_path

    # Set the file attribute to make it writable again
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0)  # 0 corresponds to normal attributes

    # Remove read only tag to title
    current_title = root.title()
    new_title = current_title.replace(" - [READ-ONLY]", "")
    root.title(new_title)

def sentence_case():
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    if selected_text:
        lines = selected_text.splitlines()
        sentence_cased_text = []
        for line in lines:
            sentences = re.split(r'(?<=[.!?])\s+', line)
            sentence_cased_sentences = []
            for sentence in sentences:
                if sentence:
                    sentence = sentence[0].capitalize() + sentence[1:]
                sentence_cased_sentences.append(sentence)
            sentence_cased_line = ' '.join(sentence_cased_sentences)
            sentence_cased_text.append(sentence_cased_line)
        sentence_cased_text = '\n'.join(sentence_cased_text)
        text.replace(tk.SEL_FIRST, tk.SEL_LAST, sentence_cased_text)


def sentence_case_with_bullets():
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    if selected_text:
        lines = selected_text.splitlines()
        capitalized_lines = []
        for line in lines:
            if len(line) >= 3:
                # Capitalize the third character in the line
                line = line[:2] + line[2].capitalize() + line[3:]
            capitalized_lines.append(line)
        capitalized_text = '\n'.join(capitalized_lines)

        # copied from sentence_case():
        sentence_cased_text = []
        for line in capitalized_lines:
            sentences = re.split(r'(?<=[.!?])\s+', line)
            sentence_cased_sentences = []
            for sentence in sentences:
                if sentence:
                    sentence = sentence[0].capitalize() + sentence[1:]
                sentence_cased_sentences.append(sentence)
            sentence_cased_line = ' '.join(sentence_cased_sentences)
            sentence_cased_text.append(sentence_cased_line)
        sentence_cased_text = '\n'.join(sentence_cased_text)
        text.replace(tk.SEL_FIRST, tk.SEL_LAST, sentence_cased_text)



def open_dropped_text_file(event):
    global current_file_path
    file_path = event.data
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)  # Clear the current content
            text.insert(tk.END, file.read())  # Insert file content into the Text widget
        current_file_path = file_path
        file_name = os.path.basename(file_path)
        root.title(f"{file_name} - Editor")

        if is_read_only():
            set_attribute_readonly()
        else:
            set_attribute_normal()


def change_cursor(event):
    event.widget.config(cursor="copy")

def reset_cursor(event):
    event.widget.config(cursor="")



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

        if is_read_only():
            set_attribute_readonly()
        else:
            set_attribute_normal()

def save_file(event=None):
    global current_file_path

    if current_file_path:
        if is_read_only():
            messagebox.showerror("Read-only Error","Cannot save Read-only file.")
        else:
            with open(current_file_path, 'w') as file:
                file.write(text.get(1.0, tk.END))
    else:
        # Check if the first line of the text starts with '#'
        first_line = text.get(1.0, 1.0 + len("#") + 1)  # Get the first line
        if first_line.strip().startswith('#'):
            # Extract the suggested file name, convert to lowercase, replace spaces with underscores, and remove hashtags
            suggested_file_name = first_line.replace('#', '').strip().replace(' ', '_').lower()
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=suggested_file_name)
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        
        if file_path:
            with open(file_path, 'w') as file:
                file.write(text.get(1.0, tk.END))
            # Get the file name from the file path
            file_name = os.path.basename(file_path)
            root.title(f"{file_name} - Editor")
            current_file_path = file_path  # Update current_file_path

def save_as_file():
    global current_file_path
    # Check if the first line of the text starts with '#'
    first_line = text.get(1.0, 1.0 + len("#") + 1)  # Get the first line
    if first_line.strip().startswith('#'):
        # Extract the suggested file name, convert to lowercase, replace spaces with underscores, and remove hashtags
        suggested_file_name = first_line.replace('#', '').strip().replace(' ', '_').lower()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=suggested_file_name)
    else:
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
root = TkinterDnD.Tk()
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

# Create vertical scrollbar
vertical_scrollbar = tk.Scrollbar(root, command=text.yview)
vertical_scrollbar.pack(side="right", fill="y")
text.config(yscrollcommand=vertical_scrollbar.set)

# Create horizontal scrollbar
#horizontal_scrollbar = tk.Scrollbar(root, orient="horizontal", command=text.xview)
#horizontal_scrollbar.pack(side="bottom", fill="x")
#text.config(xscrollcommand=horizontal_scrollbar.set)

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
edit_menu.add_command(label="Sentence Case", command=sentence_case)
edit_menu.add_command(label="Sentence Case (With Bullets)", command=sentence_case_with_bullets)
edit_menu.add_command(label="Insert Bullets", command=add_bullets)
edit_menu.add_command(label="Insert Tabs", command=add_tabs)
edit_menu.add_command(label="Set Attribute Read-Only ", command=set_attribute_readonly)
edit_menu.add_command(label="Set Attribute Normal ", command=set_attribute_normal)
edit_menu.add_command(label="Prepend Lines with Input", command=prepend_lines_with_input)
edit_menu.add_command(label="Find and Replace in Selection", command=find_replace_in_selection)

# edit_menu.add_separator()
# edit_menu.add_command(label="Find and Replace", command=lambda: find_replace.open_find_replace(root, text))


# Bind hotkeys
text.bind("<Control-n>", new_file)
text.bind("<Control-s>", save_file)
text.bind("<Control-o>", open_file)
text.bind("<Control-BackSpace>", delete_word_backwards)



# Register the Text widget as a drop target for text files
text.drop_target_register(DND_FILES)
text.dnd_bind('<<Drop>>', open_dropped_text_file)


# Create a toolbar
toolbar = tk.Frame(root)
toolbar.pack(fill="x")

# Add a button to capitalize selected text
capitalize_button = tk.Button(toolbar, text="Capitalize", command=capitalize_selected_text)
capitalize_button.pack(side="left")

# open any files that were passed to it as arguments
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Assuming you have a function like open_file(file_path)
        #open_file(file_path)

        if file_path:
            with open(file_path, 'r') as file:
                text.delete(1.0, tk.END)
                text.insert(tk.END, file.read())
            # Get the file name from the file path
            file_name = os.path.basename(file_path)
            root.title(f"{file_name} - Editor")
            current_file_path = file_path

            if is_read_only():
                set_attribute_readonly()
            else:
                set_attribute_normal()

        current_file_path = file_path  # Update the current file path

# Run the main loop
root.mainloop()
