
import os
import hashlib
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, scrolledtext

def hash_file(file_path):
    """Generate MD5 hash for a file"""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def delete_by_extension(directory, extension, log_box):
    deleted = False
    for folder, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(folder, file)
            if file_path.lower().endswith(extension.lower()):
                try:
                    os.remove(file_path)
                    log_box.insert(END, f"🗑️ Deleted (by ext): {file_path}\n")
                    deleted = True
                except Exception as e:
                    log_box.insert(END, f"⚠️ Error deleting {file_path}: {e}\n")
    if not not deleted:
        log_box.insert(END, f"No files with extension {extension} found.\n")

def remove_duplicates(directory, log_box):
    hash_map = {}
    duplicates = []
    for folder, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(folder, file)
            try:
                file_hash = hash_file(file_path)
                if file_hash in hash_map:
                    os.remove(file_path)
                    log_box.insert(END, f"🗑️ Duplicate removed: {file_path}\n")
                    duplicates.append(file_path)
                else:
                    hash_map[file_hash] = file_path
            except Exception as e:
                log_box.insert(END, f"⚠️ Error reading {file_path}: {e}\n")
    if not duplicates:
        log_box.insert(END, "🎉 No duplicates found.\n")

def browse_directory(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, END)
        entry.insert(0, folder)

def start_cleanup(dir_entry, ext_entry, mode_var, log_box):
    directory = dir_entry.get().strip()
    extension = ext_entry.get().strip()

    if not os.path.exists(directory) or not os.path.isdir(directory):
        messagebox.showerror("Error", "Please select a valid directory")
        return

    log_box.insert(END, f"\n🔍 Scanning: {directory}\n")
    log_box.see(END)

    if mode_var.get() == "ext":
        if not extension.startswith("."):
            messagebox.showerror("Error", "Please enter a valid extension (e.g., .txt)")
            return
        delete_by_extension(directory, extension, log_box)
    elif mode_var.get() == "dup":
        remove_duplicates(directory, log_box)

    log_box.insert(END, "✅ Task completed.\n")
    log_box.see(END)

# ---------------- GUI ---------------- #
root = tb.Window(themename="cosmo")  # modern theme
root.title("✨ Atharv's File Cleaner ✨")
root.geometry("750x550")
root.resizable(False, False)

title_label = tb.Label(root, text="File Cleaner-By Atharv ", 
                       font=("Segoe UI", 18, "bold"), bootstyle="primary")
title_label.pack(pady=15)

# Directory selection
frame1 = tb.Frame(root)
frame1.pack(fill="x", padx=20, pady=10)

tb.Label(frame1, text="Select Directory:", font=("Segoe UI", 11)).pack(anchor="w")
dir_entry = tb.Entry(frame1, width=65, bootstyle="info")
dir_entry.pack(side="left", padx=5, pady=5)
tb.Button(frame1, text="📂 Browse", bootstyle="primary-outline",
          command=lambda: browse_directory(dir_entry)).pack(side="left", padx=5)

# Mode selection
mode_var = tb.StringVar(value="ext")
frame2 = tb.Labelframe(root, text="Cleanup Mode", bootstyle="info")
frame2.pack(fill="x", padx=20, pady=10)

tb.Radiobutton(frame2, text="Delete by Extension", variable=mode_var, value="ext", bootstyle="success").pack(side="left", padx=20, pady=5)
tb.Radiobutton(frame2, text="Remove Duplicates", variable=mode_var, value="dup", bootstyle="danger").pack(side="left", padx=20, pady=5)

# Extension input
frame3 = tb.Frame(root)
frame3.pack(fill="x", padx=20, pady=10)
tb.Label(frame3, text="Extension (e.g. .txt):", font=("Segoe UI", 11)).pack(side="left")
ext_entry = tb.Entry(frame3, width=12, bootstyle="info")
ext_entry.pack(side="left", padx=10)

# Start button
tb.Button(root, text="🚀 Start Cleanup", bootstyle="success",
          command=lambda: start_cleanup(dir_entry, ext_entry, mode_var, log_box)).pack(pady=10)

# Log area
log_label = tb.Label(root, text="Logs:", font=("Segoe UI", 12, "bold"))
log_label.pack(anchor="w", padx=20)

log_box = scrolledtext.ScrolledText(root, width=85, height=15, font=("Consolas", 10))
log_box.pack(padx=20, pady=10)

# Run
root.mainloop()
