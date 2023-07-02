#Auto-updating formatting for Arma3 Mods with filter
#Made by: Slyrex/Slyrem
# v4.0
# Update log: v1.0 - Initial release v2.0 - Added GUI v3.0 - Added save settings v4.0 - Added load settings
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import json

# Settings file to remember paths and unfiltered mods
script_directory = os.path.dirname(os.path.abspath(__file__))
path_to_settings_file = os.path.join(script_directory, 'settings.json')

# Load Settings
try:
    with open(path_to_settings_file, 'r') as file:
        settings = json.load(file)
except FileNotFoundError:
    settings = {
        "path_to_mods": "",
        "path_to_parameter_file": "",
        "unfiltered_mods": [],
        "mods": []
    }

def select_mods_directory():
    settings["path_to_mods"] = filedialog.askdirectory()
    refresh_mod_list()
    save_settings()

def select_parameter_file():
    settings["path_to_parameter_file"] = filedialog.askopenfilename()
    save_settings()

def save_settings():
    with open(path_to_settings_file, 'w') as file:
        json.dump(settings, file)

# GUI start
window = tk.Tk()
window.title("Slyrex Arma3 Mod Filteration")

# Buttons to select directories
select_mods_dir_button = tk.Button(window, text="Select Mods Directory", command=select_mods_directory)
select_mods_dir_button.pack(padx=10, pady=10)

select_parameter_file_button = tk.Button(window, text="Select Parameter File", command=select_parameter_file)
select_parameter_file_button.pack(padx=10, pady=10)

# List of mods
listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
listbox.pack(padx=10, pady=10)

def refresh_mod_list():
    # Clear the listbox
    listbox.delete(0, tk.END)
    
    # Get a list of all folders in the mods directory
    settings["mods"] = os.listdir(settings["path_to_mods"]) if settings["path_to_mods"] else []

    # Filter out any files, we only want directories
    settings["mods"] = [mod for mod in settings["mods"] if os.path.isdir(os.path.join(settings["path_to_mods"], mod))]

    # Populate it with the mod names
    for mod in settings["mods"]:
        listbox.insert(tk.END, mod)

        # If the mod was unfiltered in the last run, select it in the listbox
        if mod in settings["unfiltered_mods"]:
            listbox.selection_set(tk.END)

refresh_mod_list()

def update_param_file():
    # Select mods
    selected_mods = [listbox.get(i) for i in listbox.curselection()]
    
    # Filter mods
    filtered_mods = [mod for mod in settings["mods"] if mod not in selected_mods]
    
    # Formatting for the parameters file
    formatted_mods = ';'.join(['@' + mod for mod in filtered_mods])
    
    # Read params file
    with open(settings["path_to_parameter_file"], 'r') as file:
        lines = file.readlines()
    
    # Find mods= line and update it
    for i, line in enumerate(lines):
        if line.startswith('mods='):
            lines[i] = 'mods=' + formatted_mods + '\n'
    
    # Write the formattings back to the params file
    with open(settings["path_to_parameter_file"], 'w') as file:
        file.writelines(lines)
    
    # Save the unfiltered mods
    settings["unfiltered_mods"] = selected_mods
    save_settings()
    
    # Show a message box to confirm
    messagebox.showinfo("UwU We have gone and done it", "The parameter file has been updated successfully!")

# Create a button that will call the update_param_file function when clicked
update_button = tk.Button(window, text="Update Parameter File", command=update_param_file)
update_button.pack(padx=10, pady=10)

window.mainloop()
