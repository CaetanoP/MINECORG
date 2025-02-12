import click
from pathlib import Path
from ..utils import file_utils
from . import project
from ..classes import entity


@click.command()
def create():
    """
    Create a new entity.
    """
    ## Register the basic entities components
    ## entity.name, entity.id, entity.geometry, entity
    new = entity.Entity(click.prompt("Please enter the name of the entity"))
    click.echo(f"Entity created with name: {new.name}")
    
    ## Request the Model
    list.invoke(click.Context(list))
    ## Request the Texture
    
    ## Create the RenderController
    
    ## Create the Entity RP
    
    ## Create the Entity BP
    
    click.echo("Entity Created")

def entity_model_request() -> bool:
    """
    Search for {entity.name}.geo.json file in models folder
    """
    path = "awdwa"
    file_name = "entity.name.geo.json"
    target = file_utils.find_file(path,file_name)
    if target != None:
        #if the json file exist modify it
        
        
        
        return True
    return False

@click.command()
@click.option('--entity', is_flag=True)
def list(entity :bool,):
    """
    List all entities
    """
    try:
        entities_dir = Path(project.PROJECT_DIRECTORY) / "behavior_packs" / "dant_myal" / "entities"
        click.echo(click.style("Scanning entity vault...", fg="yellow", bold=True))
        
        files = file_utils.find_files(entities_dir)
        
        if not files:
            click.echo(click.style("\nWhoops! No entities found in the workshop!", fg="red"))
            return

        # Header
        click.echo("\n" + click.style("Available Entities ({}):".format(len(files)), 
        fg="cyan", bold=True, underline=True))
        
        # List entities with Minecraft-style formatting
        for idx, file in enumerate(files, 1):
            file_path = Path(file)
            file_name = file_path.stem.replace('_', ' ').title()
            click.echo(
                click.style(f"#{idx} ", fg="magenta") + 
                click.style(file_name, fg="bright_green", bold=True) + 
                click.style(f" [ {file_path.name} ]", fg="white")
            )

        # Footer
        click.echo("\n" + click.style("Found ", fg="bright_white") + 
        click.style(str(len(files)), fg="yellow", bold=True) + 
        click.style(" awesome entities ready for action!", fg="bright_white"))

    except FileNotFoundError:
        click.echo(click.style("\nAlert! Entity workshop directory missing!", fg="red", bold=True))
        click.echo(click.style("Did you forget to build the castle first?", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"\nCritical Crash! {str(e)}", fg="red", bold=True))
        click.echo(click.style("Quick! Call the Minecraft engineers!", fg="bright_red"))
    

def remove():
    """
    Remove an existing entity.
    """
    ...

def scan():
    """
    Verify if an entity have all component needed
    """
    ...
