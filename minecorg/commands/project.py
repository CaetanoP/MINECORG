import click
import os
import json
from pathlib import Path
import shutil
from ..utils import file_utils

PROJECT_DIRECTORY: str = os.getcwd()

def get_mod_info():
    try:
        with open(Path(os.getcwd()) / "minecorg.json") as f:
            data = json.load(f)
            mod_name = data.get("mod_name")
            namespace = data.get("namespace")
            return mod_name, namespace  # Return the values as a tuple
    except (FileNotFoundError, json.JSONDecodeError):
        a = " "
        return a, a

# Usage
MOD_NAME, NAMESPACE = get_mod_info()

#Help Functions
def create_folder_structure(base_structure, target_path, variables):
    """
    Recursively creates a folder and file structure based on a given template.
    Args:
        base_structure (dict): A dictionary representing the folder and file structure.
                               Keys are folder or file names, and values are either "file" 
                               or another dictionary representing subfolders and files.
        target_path (Path): The base path where the folder structure will be created.
        variables (dict): A dictionary of variables to replace placeholders in folder and file names.
    """
    
    for name, content in base_structure.items():
        # Replace placeholders in names
        formatted_name = name.format(**variables)
        new_path = target_path / formatted_name
        
        if content == "file":
            new_path.touch()
            click.echo(f"Created file: {new_path}")
        elif isinstance(content, dict):
            new_path.mkdir(parents=True, exist_ok=True)
            click.echo(f"Created directory: {new_path}")
            create_folder_structure(content, new_path, variables)

#Commands
@click.command()
@click.option("--path", prompt="Project root path", type=click.Path(file_okay=False))
def init(path):
    """
    Initializes a new Minecraft mod project at the specified path.
    This function collects metadata from the user, creates the root project directory,
    loads a folder structure template, creates the folder structure, and saves the 
    metadata to a JSON file.
    Args:
        path (str): The path where the project should be initialized.
    Raises:
        FileNotFoundError: If the folder structure template file is not found.
        OSError: If there is an error creating the project directory or writing the metadata file.
    Notes:
        - The user is prompted to input the project name, mod name, and namespace.
        - The folder structure is defined in a JSON template file.
        - Metadata is stored in a 'metadata.json' file within the project root directory.
    """
    #Preciso melhorar essa função verificando se existe alguma coisa na pasta de criação e perguntando para o usuario
    # se ele realmente quer iniciar um projeto com algo na pasta
    # preciso também tirar a opção de iniciar em um path especifico, tudo sera realizado dentro do
    # diretório atual
    
    # Collect metadata
    metadata = {
        "project_name": click.prompt("Project name"),
        "mod_name": click.prompt("Mod name"),
        "namespace": click.prompt("Namespace (e.g., com.yourname)")
    }
    
    # Create root project directory
    project_root = Path(os.getcwd()) / metadata["project_name"]
    project_root.mkdir(parents=True, exist_ok=True)
    
    # Load folder structure template
    structure_template = file_utils.load_template_file("folder_structure.json")
    # Create folder structure
    create_folder_structure(structure_template, project_root, metadata)
    # Save metadata
    metadata_path = project_root / "minecorg.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
        
    click.echo(f"\nProject created successfully at {project_root}",color="green")
    click.echo(f"Metadata stored in {metadata_path}")
    

@click.command()
def load():
    """
    This command collects metadata from the user and creates a 'minecorg.json' file in the current working directory.
    The metadata includes the project name, mod name, and namespace. This file can be used to store and manage 
    project-specific information for a Minecraft mod project.
    """  
    #Preciso melhorar essa função ela precisa scanear o folder mostrar oq esta faltando e perguntar ao
    # usuario se deseja continuar assim mesmo ou adicionar as pastas que faltam, depois ele ira procurar no
    # projeto alguma maneira de descobrir o namespace utilizado, nome do mod e namespace
    # Collect metadata
    metadata = {
        "project_name": click.prompt("Project name"),
        "mod_name": click.prompt("Mod name"),
        "namespace": click.prompt("Namespace (e.g., com.yourname)")
    }
    
    # Save metadata
    metadata_path = Path(os.getcwd()) / "minecorg.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
        
    click.echo(f"\nMetadata stored in {metadata_path}")
    
    

def list(model:bool,texture:bool,object:str):
    files = []
    packs = []
    if model:
        files.append("models")
        packs.append("resource_packs")
    if texture:
        files.append("textures")
        packs.append("resource_packs")
        
        
    for i in range(len(files)):
        try:
            dir = Path(PROJECT_DIRECTORY) / packs[i] / str(MOD_NAME) / files[i] / object
            click.echo(click.style(f"\nScanning {files[i]} for {object} in {packs[i]}...", fg="yellow", bold=True))
            
            files_dir = file_utils.find_files(dir)
            
            if not files:
                click.echo(click.style(f"\nWhoops! No {object} found in the workshop!", fg="red"))
                return

            # Header
            click.echo("\n" + click.style("Available "+files[i]+" ({}):".format(len(files_dir)), 
            fg="cyan", bold=True, underline=True))
            
            # List entities with Minecraft-style formatting
            for idx, file in enumerate(files_dir, 1):
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
    

    
    
    
@click.command()
@click.option('-m','--model', is_flag=True)
@click.option('-t','--texture',is_flag = True)
def listEntity(model:bool,texture:bool):
    list(model=model,texture=texture,object="entity")
    ...
    
    
@click.command()
@click.option('-m','--model', is_flag=True)
@click.option('-t','--texture',is_flag = True)
def listBlock(model : bool, texture:bool ):
    list(model=model,texture=texture,object="blocks")
    ...
       

    
    
    
    
    
    
    
    
    
    
    
@click.command()
@click.option('--entity', is_flag=True)
@click.option('--block',is_flag=True)
def listawd(entity :bool,):
    """
    --entity list bp/entities
    --entity -m list rp/models/entity
    --entity -t list rp/textures/entity
    --block list bp/blocks
    --block -m list rp/models/blocks
    """
    
    
    
    try:
        entities_dir = Path(PROJECT_DIRECTORY) / "behavior_packs" / str(MOD_NAME) / "entities"
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