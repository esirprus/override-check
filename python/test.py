import os
import xml.etree.ElementTree as ET
from myfunction import extract_attr
def process_mod(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        print(f"Checking XML files in folder: {folder_path}")

        # Lists to store identifiers and species names
        identifiers = []
        speciesnames = []

        # Iterate over all subdirectories and files within the folder
        for root_dir, _, files in os.walk(folder_path):
            for xml_filename in files:
                if xml_filename.endswith(".xml"):
                    xml_file_path = os.path.join(root_dir, xml_filename)
                    folder_tree = ET.parse(xml_file_path)
                    folder_root = folder_tree.getroot()
                    all_elements = [folder_root]+folder_tree.findall(".//*")

                    # Iterate through all elements in the XML file
                    for element in all_elements:
                        if element.tag.lower() == 'override':
                            element_identifiers, element_speciesnames = extract_attr(element)
                            identifiers.extend(element_identifiers)
                            speciesnames.extend(element_speciesnames)

        # Return a summary of identifiers and species names as a tuple
        return tuple(identifiers), tuple(speciesnames)

    else:
        print(f"Folder not found: {folder_path}")
        # If the folder doesn't exist, return empty tuples
        return (), ()
    

user_locale = os.getenv('LANG')
print(user_locale)
