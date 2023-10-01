import tkinter as tk
import os
from tkinter import filedialog
from pyfile import myfunction as mf, initialize as i
import json

path = i.initialize_path(os.path.abspath(__file__))
locale_f = i.load_locale_file(path["locales_folder_path"])
print(locale_f)
root = tk.Tk()
root.withdraw()
#welcome message
#Optional: let user choose the localmod path to support localmod check

while True:
    choice = input(locale_f["choose"])
    if choice == "1":
        file_path = filedialog.askopenfilename(title=locale_f["modlist"])
        if file_path:
            mf.process_modlist(file_path, path["local_folder_path"])
        else:
            print(locale_f["no_selected"])
    elif choice == "2":
        folder_path = filedialog.askdirectory(title=locale_f["modfolder"])
        if folder_path:
            mf.process_mod(folder_path)
        else:
            print(locale_f["no_selected"])
    elif choice.lower() == "q":
        print(locale_f["quit"])
        break
    elif choice.lower() == "f":
        file_path = filedialog.askdirectory(title=locale_f["localmod"])
        if file_path:
            path["local_folder_path"] = file_path
            with open(path["path_file_path"], 'w') as file:
                json.dump(path, file)
            print(locale_f["localmod_success"])
        else:
            print(locale_f["no_selected"])
    else:
        print(locale_f["invalid"])