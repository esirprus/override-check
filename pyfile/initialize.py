#this module is used to initialize the path and load the locale file and user data
import os
import json
from .myfunction import load_json
# Function to initialize path, load first.
def initialize_path(main_file_path):
    project_folder_path = os.path.dirname(main_file_path)
    py_folder_path = os.path.join(project_folder_path, "pyfile")
    data_folder_path = os.path.join(project_folder_path, "data")
    locales_folder_path = os.path.join(data_folder_path, "locales")
    path_file_path = os.path.join(data_folder_path, "path.json")
    if not os.path.exists(path_file_path):
        with open(path_file_path, 'w') as file:
            pass
    if os.path.getsize(path_file_path) == 0:
        path_dict = {
            "project_folder_path": project_folder_path,
            "py_folder_path": py_folder_path,
            "data_folder_path": data_folder_path,
            "locales_folder_path": locales_folder_path,
            "path_file_path": path_file_path,
            "local_folder_path": None
        }
        with open(path_file_path, 'w') as file:
            json.dump(path_dict, file, indent=4)
    path = load_json(path_file_path)
    return path

#Get language and return the dictionary,need to load second because it need the path from initialize_path
def load_locale_file(locales_folder_path):
    env = os.getenv("LANG")
    lang = env.split('.')[0].split('_')[0]
    if lang != "zh":
        lang = "en"
    lang_file = lang + ".json"
    locale_file = load_json(os.path.join(locales_folder_path, lang_file))
    return locale_file

#TODO:move this to main.py
'''
def initialize_user_data(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            user_data = json.load(file)
            print(local_f["mf"]["load"])
            print(f"Local Path: {user_data['local_path']}")
    else:
        input("It seems this is your first time using this program, please select your local path: ")
        root = tk.Tk()
        root.withdraw()
        local_path = filedialog.askdirectory(title="Select a local path")
        # Store the local path in the JSON file
        user_data_dict = {
            'local_path': local_path
        }

        with open(json_file_path, 'w') as file:
            json.dump(user_data_dict, file)
            print("Data stored successfully!")
        with open(json_file_path, 'r',encoding='utf-8') as file:
            user_data = json.load(file)
    return user_data
'''