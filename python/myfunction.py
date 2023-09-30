import os
import json
import tkinter as tk
from tkinter import filedialog
from lxml import etree #try use lxml instead of xml
import locale

#TODO:add language support
#TODO:modify prcess_mod 
#FIXME? fix "/" and "\" problem
#TODO:use lxml xpath to find case insensitive tag


# Function to initialize path
def initialize_path():
    py_folder_path = os.path.dirname(os.path.abspath(__file__))
    project_folder_path = os.path.join(py_folder_path, "..")
    data_folder_path = os.path.join(project_folder_path, "data")
    os.makedirs(data_folder_path, exist_ok=True)
    json_file_path = os.path.join(data_folder_path, "user_data.json")
    locales_folder_path = os.path.join(project_folder_path, "locales")
    os.makedirs(locales_folder_path, exist_ok=True)
    return {
        "project_folder_path": project_folder_path,
        "py_folder_path": py_folder_path,
        "data_folder_path": data_folder_path,
        "json_file_path": json_file_path,
        "locales_folder_path": locales_folder_path
    }
#test
#print(initialize_path())

#fuction to get user data
def initialize_user_data(json_file_path):
    if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
        with open(json_file_path, 'r') as file:
            user_data = json.load(file)
            print("Welcome back! Your data:")
            print(f"Local Path: {user_data['local_path']}")
    else:
        input("Please select your local path: ")
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

#function to get language and return the dictionary
def load_locale_file(locales_folder_path):
    env = os.getenv("LANG")
    lang = env.split('.')[0].split('_')[0]
    if lang != "zh":
        lang = "en"
    lang_file = lang + ".json"
    with open(os.path.join(locales_folder_path,lang_file),'r',encoding='utf-8') as f:
        locale_file = json.load(f)
    return locale_file

def extract_attr(element):
    identifiers = []
    speciesnames = []

    for child in element:
        if child.attrib:
            for attrib in child.attrib:
                if attrib.lower() == 'identifier':
                    identifiers.append(child.attrib[attrib])
                elif attrib.lower() == 'speciesname':
                    speciesnames.append(child.attrib[attrib])
        # Check if the direct child element has no attributes
        else:
            for grandchild in child:
                for attrib in grandchild.attrib:
                    if attrib.lower() == 'identifier':
                        identifiers.append(grandchild.attrib[attrib])
                    elif attrib.lower() == 'speciesname':
                        speciesnames.append(grandchild.attrib[attrib])

    return identifiers, speciesnames

# Function to process modlist.xml
#Optional Features: if local_path is not None, then it will also process the local mod
def process_modlist(file_path,local_path):
    tree = etree.parse(file_path)
    root = tree.getroot()
    username = os.getenv('USERNAME')
    for workshop in root.findall(".//Workshop"):
        name = workshop.get("name")
        id = workshop.get("id")
        print(f"Workshop Name: {name}, ID: {id}")

        # Define the folder path for the workshop's XML files
        #TODO: Check if this works on Linux and Mac

        workshop_folder = os.path.join(
            "C:\\Users",
            username,
            "AppData",
            "Local",
            "Daedalic Entertainment GmbH",
            "Barotrauma",
            "WorkshopMods",
            "Installed",
            id,
        )
        if os.path.exists(workshop_folder):
            process_mod(workshop_folder)
        else:
            print(f"Folder not found for ID: {id},please check if the workshop mod is installed.")
    if local_path:
        for local in root.findall(".//Local"):
            name = local.get("name")
            print(f"Local Name: {name}")
            local_mod_folder = os.path.join(local_path,name)
            if os.path.exists(local_mod_folder):
                process_mod(local_mod_folder)
            else:
                print(f"Folder not found for Local mod.")

# Function to check a single folder
def process_mod(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        print(f"Checking XML files in folder: {folder_path}")

        # Iterate over all subdirectories and files within the workshop folder
        for root_dir, _, files in os.walk(folder_path):
            for xml_filename in files:
                if xml_filename.endswith(".xml"):
                    xml_file_path = os.path.join(root_dir, xml_filename)
                    folder_tree = etree.parse(xml_file_path)
                    folder_root = folder_tree.getroot()
                    all_elements = [folder_root]+folder_tree.findall(".//*")
                    identifiers = []
                    speciesnames = []

                    for element in all_elements:
                        if element.tag.lower() == 'override':
                            element_identifiers, element_speciesnames = extract_attr(element)
                            identifiers.extend(element_identifiers)
                            speciesnames.extend(element_speciesnames)

                    if identifiers or speciesnames:
                        print(f"File: {xml_filename} has <override> element!")
                    if identifiers:
                        print(f"Identifiers: {', '.join(identifiers)}")
                    if speciesnames:
                        print(f"Speciesnames: {', '.join(speciesnames)}")

    else:
        print(f"Folder not found: {folder_path}")

