import click
import os
import json
from pathlib import Path

def load_base_structure():
    """Load the base folder structure from a JSON file."""
    try:
        base_structure_path = Path(__file__).parent.parent / "templates/folder_structure.json"  
        with open(base_structure_path, "r") as f:
            return json.load(f)
    except:
        print("There is no json file for base project structure or the directory is wrong")
    

def scan_folder_structure(base_structure, target_path, missing_items):
    """Recursively scan the folder structure and identify missing items."""
    for item, item_type in base_structure.items():
        item_path = target_path / item
        if item_type == "file":
            if not item_path.is_file():
                missing_items.append(str(item_path))
        elif isinstance(item_type, dict):
            if not item_path.is_dir():
                missing_items.append(str(item_path))
            else:
                scan_folder_structure(item_type, item_path, missing_items)

@click.command()
@click.argument("target_path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def scan(target_path):
    """Scan a folder and identify missing items compared to the base structure."""
    base_structure = load_base_structure()
    missing_items = []
    target_path = Path(target_path)

    # Perform the scan
    scan_folder_structure(base_structure, target_path, missing_items)

    # Display results
    if missing_items:
        click.echo("The following items are missing:")
        for item in missing_items:
            click.echo(f"- {item}")
    else:
        click.echo("The folder structure is complete!")
        
if __name__ == "__main__":
    scan()