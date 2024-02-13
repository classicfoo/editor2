 
import tkinter as tk
from tkinter import filedialog, simpledialog
import re
import os
import sys
from tkinterdnd2 import DND_FILES, TkinterDnD
import ctypes
from tkinter import messagebox

class AutocompleteCombobox(tk.Frame):
    def __init__(self, parent, values_commands):
        super().__init__(parent)
        self.values_commands = values_commands  # Store values and commands
        self.values = list(values_commands.keys())  # Extract just the values for display

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0)
        self.entry.bind("<KeyRelease>", self.on_keyrelease)
        self.entry.bind("<FocusIn>", highlight_selected_text)  # Bind FocusIn event to show listbox
        self.entry.bind("<FocusOut>", self.hide_listbox)  # Bind FocusIn event to hide listbox
        self.entry.bind("<Tab>", self.on_entry_tab_key)

        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=1, column=0)
        self.listbox.grid_forget()  # Initially hide the listbox
        self.listbox.bind("<Return>", self.on_return_pressed)  # Bind the <Return> key event
        self.listbox.bind("<ButtonRelease-1>", self.on_return_pressed)  # Bind the <Return> key event


        self.update_listbox()
        self.listbox.bind("<FocusOut>", self.hide_listbox)
        self.set_listbox_width_to_longest_item()


    def on_keyrelease(self, event):        
        self.update_listbox()
        self.adjust_listbox_height()  # Adjust the listbox height based on the number of items
        self.listbox.grid()  # Show the listbox
        if event.keysym == 'Down':
            # Select the first item in self.listbox
            self.listbox.focus()
            self.listbox.select_set(0)

    def on_entry_tab_key(self, event):
        #self.listbox.focus()
        self.listbox.select_set(0)
        self.listbox.select_set(0)

        #return "break"  # Prevent the Tab key press from propagating further


    def update_listbox(self):
        search_term = self.entry_var.get().lower()
        self.listbox.delete(0, tk.END)
        for item in self.values:
            if search_term in item.lower():
                self.listbox.insert(tk.END, item)

        self.set_listbox_width_to_longest_item()


    def hide_listbox(self, event=None):
        if event==None:
            # Hide the listbox when it loses focus
            self.listbox.grid_forget()
            self.entry.delete(0, tk.END)
            unhighlight_selected_text()

    def show_listbox(self, event):
        # Show the listbox when the entry is clicked again
        self.update_listbox()
        self.adjust_listbox_height()
        self.listbox.grid()
        highlight_selected_text()

    def execute_command(self, event):
        # Get the current selection from the listbox
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            data = self.listbox.get(index)
            self.entry_var.set(data)  # Set the entry field to the selected value
            self.hide_listbox()  # Hide the listbox
            command = self.values_commands.get(data)  # Get the command associated with the selected value
            if command:
                command()  # Execute the command

    def adjust_listbox_height(self):
        # Adjust the height of the listbox based on the number of items, up to a maximum
        max_height = 100  # Maximum height of the listbox
        items = self.listbox.size()
        self.listbox.config(height=min(items, max_height))

    def set_listbox_width_to_longest_item(self):
        # Iterate through all items in the listbox
        max_characters = 0
        for item in self.listbox.get(0, tk.END):
            # Calculate the number of characters in each item
            num_characters = len(item)
            if num_characters > max_characters:
                max_characters = num_characters
        
        # Add some padding (e.g., 2 characters) to the max width
        max_characters += 2
        
        # Ensure the width is at least a minimum number of characters
        minimum_width = 15
        if max_characters < minimum_width:
            max_characters = minimum_width

        # Set the width of the listbox to the maximum number of characters
        self.entry.config(width=max_characters)
        self.listbox.config(width=max_characters)

        self.adjust_listbox_height()


    def on_return_pressed(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_value = self.listbox.get(selected_index[0])
            self.entry_var.set(selected_value)
            self.execute_command(event)  # Call the on_listbox_select method

    def focus_entry(self,event=None):
        self.entry.focus()

current_file_path = None  # Initialize current_file_path as None

class FindReplaceDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Find and Replace")
        global find_str, replace_str

        # make this the default
        find_str = ","
        replace_str = ", "

        self.find_label = tk.Label(self, text="Find:")
        self.find_label.pack()

        self.find_entry = tk.Entry(self)
        self.find_entry.pack()
        self.find_entry.insert(0, find_str)

        self.replace_label = tk.Label(self, text="Replace with:")
        self.replace_label.pack()

        self.replace_entry = tk.Entry(self)
        self.replace_entry.pack()
        self.replace_entry.insert(0, replace_str)

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack()

        self.find_value = None
        self.replace_value = None

        # Bind the Enter key to the OK button
        self.bind("<Return>", self.on_ok)
        self.find_entry.bind("<FocusIn>", highlight_selected_text)

        self.focus()
        self.find_entry.focus()

    def on_ok(self,event=None):
        self.find_value = self.find_entry.get()
        self.replace_value = self.replace_entry.get()
        self.destroy()

def highlight_selected_text(event=None):
    text.tag_configure("highlight", background="#0078D7",foreground="#FFFFFF")
    if text.tag_ranges("sel"):
        selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        text.tag_add("highlight", tk.SEL_FIRST, tk.SEL_LAST)

def unhighlight_selected_text(event=None):
    if text.tag_ranges("sel"):
        selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        last = tk.SEL_LAST
        text.tag_remove("highlight", tk.SEL_FIRST, tk.SEL_LAST)
        text.focus()
        text.mark_set("insert", last)

def find_replace_in_selection(event=None):
    
    check_selection()

    # Get the current selection range
    sel_start = text.index(tk.SEL_FIRST)
    sel_end = text.index(tk.SEL_LAST + "+1c")  # Add "+1c" to include the last character

    # Get the selected text
    selected_text = text.get(sel_start, sel_end)

    highlight_selected_text()

    # Open Find Replace Dialog
    dialog = FindReplaceDialog(root)
    root.update_idletasks()  # Ensure that geometry is updated
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    dialog_width = dialog.winfo_reqwidth()
    dialog_height = dialog.winfo_reqheight()
    x = root_x + (root_width - dialog_width) // 2
    y = root_y + (root_height - dialog_height) // 2
    dialog.geometry(f"+{x}+{y}")
    root.wait_window(dialog)
    highlight_selected_text()

    global find_str, replace_str
    find_str = dialog.find_value
    replace_str = dialog.replace_value
    
    # Create a regular expression with the re.IGNORECASE flag
    pattern = re.compile(re.escape(find_str), re.IGNORECASE)

    # Perform find and replace in the selected text
    modified_text = pattern.sub(replace_str, selected_text)

    # Replace the selected text with the modified text
    text.replace(sel_start, sel_end, modified_text)

    unhighlight_selected_text()



def insert_custom_bullet():
    
    check_selection()

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

def toggle_readonly():
    if is_read_only():
        set_attribute_normal()
    else:
        set_attribute_readonly()

def sentence_case():
    
    check_selection()

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
    
    check_selection()

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

    check_selection()

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
    
    check_selection()

    # Get the selected text
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    selected_text = capitalize_first_letter_of_each_line(selected_text)
    #selected_text = capitalize_first_letter_of_each_sentence(selected_text)

    # Add bullets to non-empty lines
    formatted_text = "\n".join(["- " + line if line.strip() != "" and not line.startswith("- ") else line for line in selected_text.split("\n")])
    # Replace the selected text with the formatted text
    text.replace(tk.SEL_FIRST, tk.SEL_LAST, formatted_text)

def add_tabs():
    
    check_selection()

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

def create_toolbar(root):
    # Create a toolbar frame with a raised border
    toolbar_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
    toolbar_frame.grid(row=1, column=0, sticky="ew")

    # Dictionary of Edit menu items and their commands
    menu_commands = {
        "New": new_file,
        "Open": open_file,
        "Save": save_file,
        "Save As": save_as_file,
        "Copy Filename": copy_filename,  
        "Copy File Path": copy_file_path,  
        "Rename File": rename_file,  
        "Capitalize Every Word": capitalize_selected_text,
        "Sentence Case": sentence_case,
        "Sentence Case (With Bullets)": sentence_case_with_bullets,
        "Insert Custom Bullet": insert_custom_bullet,
        "Insert Bullets": add_bullets,
        "Insert Tabs": add_tabs,
        "Toggle Read-Only": toggle_readonly,
        "Set Attribute Read-Only": set_attribute_readonly,
        "Set Attribute Normal": set_attribute_normal,
        "Find and Replace in Selection": find_replace_in_selection,
        # Add other edit menu items and their corresponding functions here
    }

    # Create an AutocompleteCombobox widget in the toolbar
    # Pass the edit_menu_commands dictionary to the AutocompleteCombobox
    autocomplete_combobox = AutocompleteCombobox(toolbar_frame, menu_commands)
    autocomplete_combobox.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    return autocomplete_combobox

def copy_filename():
    global current_file_path

    if current_file_path:
        file_name = os.path.basename(current_file_path)
        root.clipboard_clear()  # Clear the clipboard
        root.clipboard_append(file_name)  # Append the filename to the clipboard
        root.update()  # Update the clipboard content

def rename_file():
    global current_file_path

    if current_file_path:
        existing_name = os.path.basename(current_file_path)
        new_name = tk.simpledialog.askstring("Rename", "Enter a new name:", initialvalue=existing_name)
        if new_name:
            new_path = os.path.join(os.path.dirname(current_file_path), new_name)
            try:
                os.rename(current_file_path, new_path)
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
            else:
                current_file_path = new_path
                file_name = os.path.basename(new_path)
                root.title(f"{file_name} - Editor")


def copy_file_path():
    global current_file_path
    if current_file_path:
        root.clipboard_clear()
        root.clipboard_append(current_file_path)
        #messagebox.showinfo("File Path Copied", "File path has been copied to clipboard.")


def check_selection():
    try:
        selected_range = text.tag_ranges("sel")
        if selected_range:
            start_index, end_index = selected_range
            selected_text = text.get(start_index, end_index)
        else:
            messagebox.showwarning("No Selection", "Please select some text before continuing")
    except tk.TclError as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

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
text = tk.Text(root, font=("Consolas", 11), width=1000, height=1000, wrap="word", undo=True, autoseparators=True, maxundo=-1, exportselection=False)


# Create vertical scrollbar
vertical_scrollbar = tk.Scrollbar(root, command=text.yview)
vertical_scrollbar.grid(row=2, column=1, sticky="ns")

# Configure the grid row and column weights
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

text.config(yscrollcommand=vertical_scrollbar.set)

# Connect the scrollbar to the text widget
text.config(yscrollcommand=vertical_scrollbar.set)

# Create horizontal scrollbar
#horizontal_scrollbar = tk.Scrollbar(root, orient="horizontal", command=text.xview)
#horizontal_scrollbar.pack(side="bottom", fill="x")
#text.config(xscrollcommand=horizontal_scrollbar.set)


text.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
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
file_menu.add_command(label="Save As", command=save_as_file, accelerator="Ctrl+Shift+S")
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
edit_menu.add_command(label="Insert Custom Bullet", command=insert_custom_bullet)
edit_menu.add_command(label="Find and Replace in Selection", command=find_replace_in_selection)

find_str = ""
replace_str = ""

 # Create a frame to hold the "File" menu and the custom widget
menu_frame = tk.Frame(menu)
menu_frame.grid(row=0, column=0, sticky="ew")

# Create the toolbar with AutocompleteCombobox
auto_complete_combobox = create_toolbar(root)


# Bind hotkeys
text.bind("<Control-n>", new_file)
text.bind("<Control-s>", save_file)
text.bind("<Control-o>", open_file)
text.bind("<Control-BackSpace>", delete_word_backwards)
text.bind("<FocusIn>", auto_complete_combobox.hide_listbox)

text.bind("<Control-h>", find_replace_in_selection)
text.bind("<Control-f>", find_replace_in_selection)
text.bind("<Control-p>", auto_complete_combobox.focus_entry)

# Register the Text widget as a drop target for text files
text.drop_target_register(DND_FILES)
text.dnd_bind('<<Drop>>', open_dropped_text_file)

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