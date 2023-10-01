#some useful functions
import os
from lxml import etree #try use lxml instead of xml.etree
import json

#TODO:add language support
#TODO:modify prcess_mod 
#FIXME? fix "/" and "\" problem
#TODO:use lxml xpath to find case insensitive tag

#Function to load json file,return a dictionary
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {}
    return data

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

