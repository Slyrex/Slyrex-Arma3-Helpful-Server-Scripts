# Auto-updating formatting for Arma3 Mods with filter
# Made by: Slyrex/Slyrem
# V7.0 GUI Update to make it more clean.

import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import json
from bs4 import BeautifulSoup

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
window.overrideredirect()
window.configure(bg='black')

# Creates a style, and removes border from buttons.
style = ttk.Style()
style.configure(".", relief="flat")

# Create a theme
style.theme_create("my_theme", parent="alt", settings={
    ".": {
        "configure": {
            "background": "#2b2b2b", 
            "foreground": "#e1e1e1", 
            "relief": "flat",
            "highlightthickness": 0
        }
    },
    "TLabel": {
        "configure": {
            "padding": 10,
            "font": ("Arial", 10)
        }
    },
    "TButton": {
        "configure": {
            "background": "#1e90ff",
            "padding": 10
        },
        "map": {
            "background": [("active", "#104e8b")],
            "foreground": [("active", "#ffffff")]
        }
    },
    "TCheckbutton": {
        "configure": {
            "background": "#2b2b2b",
            "foreground": "#1e90ff",
            "padding": 10
        },
        "map": {
            "background": [("active", "#1e90ff")],
            "foreground": [("active", "#ffffff")]
        }
    }
})

# Set the theme
style.theme_use("my_theme")
style.configure("TFrame", background="#2b2b2b", relief="sunken", borderwidth=1)

window.configure(background='#2b2b2b')

# Create sidebar and main frame
sidebar = ttk.Frame(window, width=200, style="TFrame")
sidebar.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=10)

main_frame = ttk.Frame(window, style="TFrame")
main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# Listbox logic to display mods global
listbox = None

# Function to refresh the listbox
def refresh_mod_list():
    global listbox
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

# Function to update the parameter file
def update_param_file():
    # Select mods
    selected_mods = [listbox.get(i) for i in listbox.curselection()]
    
    # Filter mods
    filtered_mods = [mod for mod in settings["mods"] if mod not in selected_mods]
    
    # Formatting for the parameters file
    if append_at_var.get():
        formatted_mods = ';'.join(['@' + mod for mod in filtered_mods])
    else:
        formatted_mods = ';'.join([mod for mod in filtered_mods])
    
    # Read params file
    with open(settings["path_to_parameter_file"], 'r') as file:
        lines = file.readlines()
    
    # Find -mod= line and update it
    for i, line in enumerate(lines):
        if line.startswith('-mod='):
            lines[i] = '-mod="' + formatted_mods + '"\n'
    
    # Write the formattings back to the params file
    with open(settings["path_to_parameter_file"], 'w') as file:
        file.writelines(lines)
    
    # Save the unfiltered mods
    settings["unfiltered_mods"] = selected_mods
    save_settings()
    
    messagebox.showinfo("UwU We have gone and done it", "The parameter file has been updated successfully!")

def lowercase_all_files():
    directory = filedialog.askdirectory()

    for filename in os.listdir(directory):
        lowercase_filename = filename.lower()
        try:
            os.rename(os.path.join(directory, filename), os.path.join(directory, lowercase_filename))
        except PermissionError:
            messagebox.showerror("Error", f"Couldn't rename {filename} because it is in use.")

    messagebox.showinfo("UwU We have gone and done it", "All files have been lowercase'd successfully!")

def draw_param_file_updater():
    # Clear main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Buttons to select directories
    select_mods_dir_button = ttk.Button(main_frame, text="Select Mods Directory", command=select_mods_directory)
    select_mods_dir_button.pack(padx=10, pady=10)

    select_parameter_file_button = ttk.Button(main_frame, text="Select Parameter File", command=select_parameter_file)
    select_parameter_file_button.pack(padx=10, pady=10)

    # List of mods
    global listbox
    listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE)
    listbox.pack(padx=10, pady=10)
    refresh_mod_list()

    # Checkbox to add @ to mod names
    global append_at_var
    append_at_var = tk.BooleanVar(value=False)
    append_at_checkbox = ttk.Checkbutton(main_frame, text='Add "@" to mod names in export', variable=append_at_var)
    append_at_checkbox.pack()

    # Update Param File Button
    update_button = ttk.Button(main_frame, text="Update Parameter File", command=update_param_file)
    update_button.pack(padx=10, pady=10)


def draw_extras():
    #clear main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Button to lowercase all files in a directory
    lowercase_button = ttk.Button(main_frame, text="Lowercase all files in a directory", command=lowercase_all_files)
    lowercase_button.pack(padx=10, pady=10)

def draw_modset_html_edits():
    # clear main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Button to parse HTML file
    parse_button = ttk.Button(main_frame, text="Parse HTML File", command=parse_html)
    parse_button.pack(padx=10, pady=10)

def parse_html():
    # Select HTML file
    html_file_path = filedialog.askopenfilename(filetypes=[('HTML Files', '*.html')])
    
    with open(html_file_path, 'r') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
    
    # Find mods
    mods = soup.find_all('tr', {'data-type': 'ModContainer'})
    
    # Extract the names and IDs
    results = []
    for mod in mods:
        name = mod.find('td', {'data-type': 'DisplayName'}).text
        link = mod.find('a', {'data-type': 'Link'})['href']
        id = link.split('=')[-1]  # Split the URL on '=' and take the last part
        results.append((name, id))

    # Create a new frame for the results
    results_frame = ttk.Frame(main_frame)
    results_frame.pack(padx=10, pady=10)

    # Results
    result_text = tk.Text(results_frame, wrap=tk.WORD)
    result_text.pack(padx=10, pady=10)

    # Insert the results
    for name, id in results:
        result_text.insert(tk.END, f"Name: {name}, ID: {id}\n")

    # Function to save the results
    def save_results(names=True, ids=True):
        save_file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(save_file_path, 'w') as file:
            for name, id in results:
                if names and ids:
                    file.write(f"Name: {name}, ID: {id}\n")
                elif names:
                    file.write(f"{name}\n")
                elif ids:
                    file.write(f"{id}\n")


    # Function to save results as a steamcmd batch script
    def save_steamcmd_script():
        # Prompt the user to select a directory
        messagebox.showinfo("Instructions", "Select directory you want to save your mods to")
        directory = filedialog.askdirectory(title='Select directory you want to download the mods to')

        # Prompt the user to enter a username and password
        username = simpledialog.askstring("Login name", "Enter your steam username (Use 'anoynmous' as default):")
        password = simpledialog.askstring("Password", "Enter your steam password (If you used anonymous, leave blank):", show="*")

        # Choose the file to save the results
        messagebox.showinfo("Instructions", "Save the text file, will auto add .txt to the end. Save to steamcmd folder")
        save_file_path = filedialog.asksaveasfilename(initialfile='scriptfile.txt', defaultextension=".txt")

        # Open the file and write the commands
        with open(save_file_path, 'w') as file:
            file.write(f"force_install_dir {directory}\n")
            file.write(f"login {username} {password}\n")
            for name, id in results:
                file.write(f"workshop_download_item 107410 {id} validate\n")

        # Create the path for the bat file
        dir_name = os.path.dirname(save_file_path)
        bat_file_path = os.path.join(dir_name, 'runme.bat')

        # Create the bat file
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(f'steamcmd +runscript {os.path.basename(save_file_path)}')


        messagebox.showinfo("Finished", "Finished! Run the bat file named runme.bat to download the mods!")

    # Buttons to save the results
    save_names_and_ids_button = ttk.Button(results_frame, text="Save Names and IDs", command=lambda: save_results(True, True))
    save_names_and_ids_button.pack(padx=10, pady=10)

    save_names_button = ttk.Button(results_frame, text="Save Names", command=lambda: save_results(True, False))
    save_names_button.pack(padx=10, pady=10)

    save_ids_button = ttk.Button(results_frame, text="Save IDs", command=lambda: save_results(False, True))
    save_ids_button.pack(padx=10, pady=10)
    save_steamcmd_button = ttk.Button(results_frame, text="Save as SteamCMD Script", command=save_steamcmd_script)
    save_steamcmd_button.pack(padx=10, pady=10)

# Buttons to switch between functions
switch_to_param_file_updater_button = ttk.Button(sidebar, text="Switch to Param File Updater", command=draw_param_file_updater)
switch_to_param_file_updater_button.pack(padx=10, pady=10)

switch_to_modset_html_edits_button = ttk.Button(sidebar, text="Switch to Modset HTML Edits", command=draw_modset_html_edits)
switch_to_modset_html_edits_button.pack(padx=10, pady=10)

switch_to_modset_html_edits_button = ttk.Button(sidebar, text="Extras", command=draw_extras)
switch_to_modset_html_edits_button.pack(padx=10, pady=10)

# Draw the default screen
draw_param_file_updater()

# GUI end
window.mainloop()