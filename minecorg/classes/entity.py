import click
import os
import json
class Entity():
    def __init__(self, name):
        """
        Initialize an Entity with its metadata.
        """
        self.name = name
        self.entity_id = None
        self.namespace = None
        try:
            root = os.getcwd()
            with open(os.path.join(root, 'minecorg.json'), 'r') as file:
                data = json.load(file)
                self.namespace = data.get('namespace', '')
            self.entity_id = f"{self.namespace}:{self.name}"
        except FileNotFoundError:
            raise FileNotFoundError("Initialization failed due to missing 'minecorg.json' file.")

    def __str__(self):
        """Return a string representation of the entity."""
        return f"Entity(name={self.name}, id={self.entity_id})"