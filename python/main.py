import tkinter as tk
from tkinter import filedialog
import myfunction as mf

path = mf.initialize_path()
user_data = mf.initialize_user_data(path['json_file_path'])
locale_f = mf.load_locale_file(path['locales_folder_path'])

root = tk.Tk()
root.withdraw()

while True:
    choice = input(locale_f['main.choose'])
    if choice == "1":
        file_path = filedialog.askopenfilename(title=locale_f['main.modlist'])
        if file_path:
            mf.process_modlist(file_path, user_data['local_path'])
        else:
            print(locale_f['main.no_selected'])
    elif choice == "2":
        folder_path = filedialog.askdirectory(title=locale_f['main.modfolder'])
        if folder_path:
            mf.process_mod(folder_path)
        else:
            print(locale_f['main.no_selected'])
    elif choice.lower() == "q":
        print(locale_f['main.quit'])
        break
    else:
        print(locale_f['main.invalid'])