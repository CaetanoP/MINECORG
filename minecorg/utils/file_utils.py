
import os
import json
from pathlib import Path

def find_file(folder_path, file_name):
    """
    Searches for a file with the specified name within a given folder path and its subdirectories.
    Args:
        folder_path (str): The path to the folder where the search should begin.
        file_name (str): The name of the file to search for.
    Returns:
        str: The full path to the file if found, otherwise None.
    Example:
        >>> find_file('/path/to/folder', 'example.txt')
        '/path/to/folder/subfolder/example.txt'
    Note:
        This function uses os.walk to traverse the directory tree, which can be slow for large directories.
    """
    
    for root, dirs, files in os.walk(folder_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None  # Return None if the file is not found

def load_template_file(file_name):
    
    """
    Loads a JSON template file from the 'templates' directory.
    Args:
        file_name (str): The name of the template file to load.
    Returns:
        dict: The contents of the JSON file as a dictionary if successful,
        None if the file is not found or if there is an error decoding the JSON.
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If there is an error decoding the JSON.
    """
    file_path = os.path.join(Path(__file__).parent.parent, 'templates', file_name)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_name} not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {file_name}")
        return None

def find_files(folder_path):
    """
    Returns a list of all file names in the specified folder.
    Args:
        folder_path (str or Path): The path to the folder.
    Returns:
        list: A list of file names in the folder.
    Example:
        >>> find_files('/path/to/folder')
        ['file1.txt', 'file2.txt', 'file3.txt']
    """
    if isinstance(folder_path, Path):
        folder_path = str(folder_path)
    
    try:
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    except FileNotFoundError:
        print(f"Folder {folder_path} not found")
        return []