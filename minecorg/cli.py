import click
from pathlib import Path
from .commands import create_mod
from .commands import scan
from .commands import entity
from .commands import project

#Add groups
@click.group()
def cli()->None:
    ...

@click.group()
def new()->None:
    """
    Create new objects: Entities, Items and Blocks
    """
    ...


@click.group()
def list()->None:
    ...

#cli Group
cli.add_command(scan.scan)
cli.add_command(project.init,"init")
cli.add_command(project.load)
cli.add_command(list,"list")
cli.add_command(new)

#new Group
new.add_command(entity.create,"entity")


#list Group
list.add_command(project.listEntity,"entity")
list.add_command(project.listBlock, "block")