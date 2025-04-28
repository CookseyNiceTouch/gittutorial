import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json

# Define file type mappings
FILE_TYPE_MAP = {
    'Footage': ['.mp4', '.mov', '.avi', '.mxf', '.wmv'],
    'Still Assets': ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.psd'],
    'Music': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
}

CONFIG_FILE = 'last_folders.json'

def get_category(extension):
    for category, extensions in FILE_TYPE_MAP.items():
        if extension.lower() in extensions:
            return category
    return 'Other'

def organize_files(source_dir, dest_dir, status_callback):
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    if not source_path.exists() or not source_path.is_dir():
        status_callback(f"Source directory '{source_dir}' does not exist or is not a directory.")
        return
    # Create destination subfolders
    for category in list(FILE_TYPE_MAP.keys()) + ['Other']:
        (dest_path / category).mkdir(parents=True, exist_ok=True)
    # Move files
    moved = 0
    for file in source_path.iterdir():
        if file.is_file():
            ext = file.suffix
            category = get_category(ext)
            target_folder = dest_path / category
            shutil.move(str(file), str(target_folder / file.name))
            status_callback(f"Moved {file.name} to {category}/")
            moved += 1
    status_callback(f"Organization complete! {moved} files moved.")

def load_last_folders():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                return data.get('source', ''), data.get('dest', '')
        except Exception:
            pass
    return '', ''

def save_last_folders(source, dest):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'source': source, 'dest': dest}, f)
    except Exception:
        pass

# --- Tkinter UI ---
class OrganizerApp:
    def __init__(self, root):
        self.root = root
        root.title("Project Organizer")
        # Dark mode colors
        self.bg = "#23272e"
        self.fg = "#f4f6f7"
        self.entry_bg = "#2c313a"
        self.entry_fg = "#f4f6f7"
        self.button_bg = "#FFD600"  # Bright yellow
        self.button_fg = "#23272e"  # Dark text for contrast
        self.status_bg = "#181a20"
        self.status_fg = "#f4f6f7"
        self.progress_bg = "#23272e"
        self.progress_fg = "#2980b9"
        # Set root background
        root.configure(bg=self.bg)
        # Try to set a window icon (optional, ignore if not found)
        try:
            root.iconbitmap(False, 'icon.ico')
        except Exception:
            pass
        last_source, last_dest = load_last_folders()
        self.source_var = tk.StringVar(value=last_source)
        self.dest_var = tk.StringVar(value=last_dest)
        self.font = ("Segoe UI", 11)
        # Header
        header = tk.Label(root, text="Project File Organizer", font=("Segoe UI", 16, "bold"), fg=self.fg, bg=self.bg)
        header.grid(row=0, column=0, columnspan=3, pady=(15, 10))
        # Source
        tk.Label(root, text="Source Folder:", font=self.font, fg=self.fg, bg=self.bg).grid(row=1, column=0, sticky='e', padx=(15, 5), pady=5)
        tk.Entry(root, textvariable=self.source_var, width=40, font=self.font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, relief='flat').grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_source, font=self.font, bg=self.button_bg, fg=self.button_fg, activebackground="#FFEA70", activeforeground=self.button_fg, relief='flat').grid(row=1, column=2, padx=(5, 15), pady=5)
        # Destination
        tk.Label(root, text="Destination Folder:", font=self.font, fg=self.fg, bg=self.bg).grid(row=2, column=0, sticky='e', padx=(15, 5), pady=5)
        tk.Entry(root, textvariable=self.dest_var, width=40, font=self.font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, relief='flat').grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_dest, font=self.font, bg=self.button_bg, fg=self.button_fg, activebackground="#FFEA70", activeforeground=self.button_fg, relief='flat').grid(row=2, column=2, padx=(5, 15), pady=5)
        # Progress bar (dark mode style)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", troughcolor=self.progress_bg, background=self.progress_fg, bordercolor=self.progress_bg, lightcolor=self.progress_fg, darkcolor=self.progress_bg)
        self.progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=350, style="TProgressbar")
        self.progress.grid(row=3, column=0, columnspan=3, pady=(5, 0))
        # Start button
        self.organize_btn = tk.Button(root, text="Organize", command=self.start_organize, font=("Segoe UI", 12, "bold"), bg=self.button_bg, fg=self.button_fg, activebackground="#FFEA70", activeforeground=self.button_fg, relief='flat')
        self.organize_btn.grid(row=4, column=0, columnspan=3, pady=15)
        # Status
        self.status = tk.Text(root, height=10, width=60, state='disabled', font=("Consolas", 10), bg=self.status_bg, fg=self.status_fg, relief='groove', borderwidth=2, insertbackground=self.status_fg)
        self.status.grid(row=5, column=0, columnspan=3, padx=15, pady=(0, 15))
        # Configure grid weights for resizing
        root.grid_columnconfigure(1, weight=1)
    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_var.set(folder)
    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_var.set(folder)
    def start_organize(self):
        source = self.source_var.get()
        dest = self.dest_var.get()
        if not source or not dest:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return
        self.organize_btn.config(state='disabled')
        self.status.config(state='normal')
        self.status.delete(1.0, tk.END)
        def status_callback(msg):
            self.status.insert(tk.END, msg + '\n')
            self.status.see(tk.END)
            self.status.update_idletasks()
        organize_files(source, dest, status_callback)
        self.status.config(state='disabled')
        self.organize_btn.config(state='normal')
        save_last_folders(source, dest)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizerApp(root)
    root.mainloop()
