import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox
import os

class Notepad(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Notepad")
        self.geometry("800x600")
        
        # Setting up themes
        self.current_theme = "dark"
        self.configure(bg="black")
        self.text = tk.Text(self, wrap="word", font=("Arial", 12), bg="black", fg="white", undo=True)
        self.text.pack(side="top", fill="both", expand=True)
        
        # Line numbers
        self.linenumbers = tk.Text(self, width=4, bg="gray20", fg="white", state="disabled", font=("Arial", 12))
        self.linenumbers.pack(side="left", fill="y")
        self.text.bind("<KeyRelease>", self.update_line_numbers)
        self.text.bind("<MouseWheel>", self.update_line_numbers)

        # Status bar with word count
        self.status_bar = tk.Label(self, text="", bd=1, relief="sunken", anchor="w", bg="blue", fg="white")
        self.status_bar.pack(side="bottom", fill="x")

        # Create a menu with blue background
        self.menu = tk.Menu(self, bg="blue", fg="white")
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, bg="blue", fg="white")
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = tk.Menu(self.menu, bg="blue", fg="white")
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find/Replace", command=self.find_replace)

        view_menu = tk.Menu(self.menu, bg="blue", fg="white")
        self.menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark/Light Mode", command=self.toggle_theme)

        # Track changes for undo/redo
        self.text.edit_modified(False)

    def new_file(self):
        self.text.delete("1.0", "end")
        self.title("Notepad")
        self.update_status_bar("New file created")
        self.update_line_numbers(None)

    def open_file(self):
        file = filedialog.askopenfile(parent=self, mode="r", title="Open a file")
        if file:
            contents = file.read()
            self.text.delete("1.0", "end")
            self.text.insert("1.0", contents)
            file.close()
            self.title(os.path.basename(file.name) + " - Notepad")
            self.update_status_bar("File opened: " + file.name)
            self.update_line_numbers(None)

    def save_file(self):
        current_file = self.title().split(" - ")[0]
        if current_file != "Notepad":
            with open(current_file, "w") as file:
                file.write(self.text.get("1.0", "end"))
                self.text.edit_modified(False)
                self.update_status_bar("File saved: " + current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file:
            contents = self.text.get("1.0", "end")
            file.write(contents)
            file.close()
            self.title(os.path.basename(file.name) + " - Notepad")
            self.text.edit_modified(False)
            self.update_status_bar("File saved: " + file.name)

    def cut(self):
        self.text.event_generate("<<Cut>>")
        self.update_status_bar("Text cut")

    def copy(self):
        self.text.event_generate("<<Copy>>")
        self.update_status_bar("Text copied")

    def paste(self):
        self.text.event_generate("<<Paste>>")
        self.update_status_bar("Text pasted")
        self.update_line_numbers(None)

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

    def find_replace(self):
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        replace_string = simpledialog.askstring("Replace", "Enter replacement text:")

        if find_string and replace_string:
            content = self.text.get("1.0", "end")
            new_content = content.replace(find_string, replace_string)
            self.text.delete("1.0", "end")
            self.text.insert("1.0", new_content)
            self.update_status_bar(f"Replaced '{find_string}' with '{replace_string}'")

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.configure(bg="white")
            self.text.configure(bg="white", fg="black")
            self.linenumbers.configure(bg="lightgrey", fg="black")
            self.current_theme = "light"
            self.update_status_bar("Switched to light mode")
        else:
            self.configure(bg="black")
            self.text.configure(bg="black", fg="white")
            self.linenumbers.configure(bg="gray20", fg="white")
            self.current_theme = "dark"
            self.update_status_bar("Switched to dark mode")

    def update_line_numbers(self, event):
        lines = self.text.get("1.0", "end-1c").split("\n")
        line_numbers = "\n".join(str(i + 1) for i in range(len(lines)))
        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", "end")
        self.linenumbers.insert("1.0", line_numbers)
        self.linenumbers.config(state="disabled")

    def update_status_bar(self, text):
        word_count = len(self.text.get("1.0", "end-1c").split())
        self.status_bar.config(text=f"{text} | Word Count: {word_count}")

if __name__ == "__main__":
    notepad = Notepad()
    notepad.mainloop()
