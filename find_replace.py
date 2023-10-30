import tkinter as tk

find_replace_window = None

def open_find_replace(root, text_widget):
    global find_replace_window    
    find_replace_window = tk.Toplevel(root)
    find_replace_window.title("Find and Replace")
    find_replace_window.geometry("300x120")
    center_window(find_replace_window)

    find_label = tk.Label(find_replace_window, text="Find:")
    find_label.pack()
    find_entry = tk.Entry(find_replace_window)
    find_entry.pack()

    replace_label = tk.Label(find_replace_window, text="Replace with:")
    replace_label.pack()
    replace_entry = tk.Entry(find_replace_window)
    replace_entry.pack()

    def perform_find_replace():
        find_text = find_entry.get()
        replace_text = replace_entry.get()
        if find_text:
            text_content = text_widget.get("1.0", tk.END)
            replaced_text = text_content.replace(find_text, replace_text)
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", replaced_text)
        find_replace_window.destroy()

    replace_button = tk.Button(find_replace_window, text="Replace", command=perform_find_replace)
    replace_button.pack()

    def close_find_replace_window():
        global find_replace_window
        find_replace_window.destroy()
        find_replace_window = None

    cancel_button = tk.Button(find_replace_window, text="Cancel", command=close_find_replace_window)
    cancel_button.pack()

def center_window(window):
    window_width = 300  
    window_height = 120
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")