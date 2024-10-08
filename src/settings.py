import os, json, uuid
import flet as ft
from platforms import getPlatform

# Cross-platform settings file path
if getPlatform() == "Windows":
    base_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'sdcatcher')
else:
    base_dir = os.path.join(os.path.expanduser('~'), '.sdcatcher')

# Global settings variables
SETTINGS_PATH = os.path.join(base_dir, 'settings.json')
VERSION = "0.5"
DEFAULT_SETTINGS = {
        "mappings": [],
        "showDialog": "true",
        "autoEject": "false",
        "playSound": "false",
        "version": VERSION
    }

def saveSettings(settings):
    """Saves a setting configuration to the setting path"""
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

def installSettings():
    """Creates an empty JSON schema in the user's directory."""
    
    
    os.makedirs(base_dir, exist_ok=True)  # Ensures the base directory exists
    saveSettings(DEFAULT_SETTINGS)
    print("Default settings installed successfully.")


def load():
    """Returns a dict object containing the current content of settings.json"""
    try:
        if not os.path.exists(SETTINGS_PATH):
            installSettings()
            return DEFAULT_SETTINGS

        else :       
            with open(SETTINGS_PATH) as f:
                return json.load(f)
            
    except Exception as e:
        print("Something went wrong during loading settings.json:", e)
    
    

def checkVolume():
    """Will return the dict object of the SD card mappings if a SD card is currently mounted,"""
    settings = load()
    result = []

    try:
        for mapping in settings.get("mappings", []):
            if os.path.exists(mapping["sourcePath"]):
                result.append(mapping)
        
        return result if result else False

    except Exception as e:
        print("Something wrong happened when checking mounted volumes: %s", e)



def showDialog():
    """ Boolean value for the showDialog option"""
    settings = load()
    return settings.get("showDialog", "false").lower() == "true"

############################    CREATE, MODIFY, REMOVE & GET    ##############################################################

def createNewMapping(name, sourcePath, destinationPath, type, format):
    """Adds a new mapping to the settings."""
    settings = load()
    
    new_mapping = {
        "uuid": str(uuid.uuid4()),
        "name": name,
        "sourcePath": sourcePath,
        "destinationPath": destinationPath,
        "type": type,
        "format": format
    }
    settings["mappings"].append(new_mapping)
    saveSettings(settings)
    print(f"Mapping '{name}' created successfully.")

def modifyMapping(uuid, new_mapping):
    """Modifies an existing mapping by uuid."""
    settings = load()
    
    for mapping in settings["mappings"]:
        if mapping["uuid"] == uuid :
            name = mapping["name"]
            mapping.update(new_mapping)
            saveSettings(settings)
            print(f"Mapping '{name}' modified successfully.")
            return
    
    print(f"Mapping not found. 1")

def removeMapping(uuid):
    """Removes a mapping by uuid."""
    settings = load()
    newMappings = []
    for mapping in settings["mappings"] :
        if mapping["uuid"] != uuid :
            newMappings.append(mapping)
    
    if len(newMappings) == len(settings["mappings"]):
        return
    else:
        
        settings["mappings"] = newMappings
        saveSettings(settings)
        print("Mapping ",uuid," removed successfully.")

def getMapping(uuid) :
    settings = load()
    for mapping in settings["mappings"] :
        if mapping["uuid"] == uuid :
            return mapping
    print(f"Mapping not found.")
############################    IMPORT & EXPORT     ##############################################################

def importSettings(json_file_path):
    """Imports and verifies the settings from a JSON file."""
    if not os.path.exists(json_file_path):
        print(f"File '{json_file_path}' does not exist.")
        return

    with open(json_file_path, 'r') as f:
        new_settings = json.load(f)

    # Simple validation check for required fields
    required_keys = {"mappings", "showDialog", "version"}
    if not required_keys.issubset(new_settings):
        print("Invalid settings format.")
        return

    saveSettings(new_settings)
    print("Settings imported and applied successfully.")

def exportSettings(export_directory):
    """Exports the current settings to a specified directory."""
    settings = load()
    export_path = os.path.join(export_directory,"settings.json")
    with open(export_path, 'w') as f:
        json.dump(settings, f, indent=4)
    
    print(f"Settings exported to '{export_directory}' successfully.")


removeMapping("e79152f5-06c6-4fe9-87c2-c7807f5a07f2")