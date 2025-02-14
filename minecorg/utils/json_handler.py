import json
import os
from pathlib import Path


def rename_values_from_json_data(data: dict | list, old_values: list, new_values: list):
    """
    Recursively renames values in a nested dictionary or list.

    Args:
        data: The dictionary or list to process.
        old_values: A list of old values to rename.
        new_values: A list of new values to replace the old values.

    Returns:
        The modified dictionary or list.

    Raises:
        ValueError: If old_values and new_values have different lengths.
    """
    # Validate input lengths
    if len(old_values) != len(new_values):
        raise ValueError("old_values and new_values must have the same length.")

    # Create a mapping dictionary for O(1) lookups
    replacement_dict = {old: new for old, new in zip(old_values, new_values)}

    def _recursive_rename(data):
        if isinstance(data, dict):
            return {k: _recursive_rename(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [_recursive_rename(item) for item in data]
        else:
            return replacement_dict.get(
                data, data
            )  # Replace if found, else return original

    return _recursive_rename(data)


def import_data_from_json_file_template(file_name: str) -> dict:
    """
    Imports data from a JSON file located in the 'templates' directory.
    This function constructs the path to the JSON file based on the provided
    file name and attempts to read and parse the JSON content. If the file
    is not found or if there is an error decoding the JSON, it handles the
    exceptions gracefully and returns an empty dictionary.
    Args:
        file_name (str): The name of the JSON file to import.
    Returns:
        dict: The parsed JSON data as a dictionary. Returns an empty dictionary
                if the file is not found or if there is an error decoding the JSON.
    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If there is an error decoding the JSON content.
    """

    template_path = os.path.join(Path(__file__).parent.parent, "templates", file_name)
    try:
        with open(template_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_name} not found at {template_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {file_name}")
        return {}
    return {}
    ...


def rename_key_from_json_data(data, old_key, new_key):
    """
    Recursively renames a key in a nested dictionary or list.

    :param data: The dictionary or list to process.
    :param old_key: The key to rename.
    :param new_key: The new key name.
    :return: The modified dictionary or list.
    """
    if isinstance(data, dict):
        # If the old_key exists in the current dictionary, rename it
        if old_key in data:
            data[new_key] = data.pop(old_key)
        # Recursively process all values in the dictionary
        for key, value in data.items():
            data[key] = rename_key_from_json_data(value, old_key, new_key)
    elif isinstance(data, list):
        # Recursively process all items in the list
        for i, item in enumerate(data):
            data[i] = rename_key_from_json_data(item, old_key, new_key)
    return data


def rename_values_from_json_file(file_path: str, old_values: list, new_values: list):
    """
    Renames values in a JSON file and saves the modified content back to the file.

    Args:
        file_path: The path to the JSON file.
        old_values: A list of old values to rename.
        new_values: A list of new values to replace the old values.

    Raises:
        ValueError: If old_values and new_values have different lengths.
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If there is an error decoding the JSON content.
    """
    # Read the JSON data from the file
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Error decoding JSON", file_path, 0)

    # Rename the values in the JSON data
    modified_data = rename_values_from_json_data(data, old_values, new_values)

    # Write the modified JSON data back to the file
    with open(file_path, "w") as file:
        json.dump(modified_data, file, indent=4)