import click
import os
import json
from pathlib import Path
import shutil
from ..utils import file_utils
from ..templates import script_template
from ..utils import json_handler

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


# Help Functions
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


# Commands
@click.command()
def init():
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
    # Collect metadata
    metadata = create_metadata()

    # Create root project directory
    project_root = Path(os.getcwd()) / metadata["project"]["name"]
    project_root.mkdir(parents=True, exist_ok=True)

    # Save metadata
    metadata_path = Path(os.getcwd())/metadata["project"]["name"]  / "minecorg.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    # Load folder structure template
    structure_template = json_handler.import_data_from_json_file_template("folder_structure.json")
    structure_template = json_handler.rename_key_from_json_data(structure_template,"mod_name",metadata["mod"]["name"])
    
    # Create folder structure
    create_folder_structure(structure_template, project_root, metadata)
    # Create scripts
    generate_just_config(metadata["project"]["name"])
    # Create env.
    create_env(metadata["project"]["name"])
    # Create package.json
    generate_package(metadata["project"]["name"])
    # Generate tfconfig
    generate_tf_config(metadata["project"]["name"])

    generate_eslint_config(metadata["project"]["name"])
    click.echo(f"\nProject created successfully at {project_root}", color="green")


def list(model: bool, texture: bool, object: str):
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
            click.echo(
                click.style(
                    f"\nScanning {files[i]} for {object} in {packs[i]}...",
                    fg="yellow",
                    bold=True,
                )
            )

            files_dir = file_utils.find_files(dir)

            if not files:
                click.echo(
                    click.style(
                        f"\nWhoops! No {object} found in the workshop!", fg="red"
                    )
                )
                return

            # Header
            click.echo(
                "\n"
                + click.style(
                    "Available " + files[i] + " ({}):".format(len(files_dir)),
                    fg="cyan",
                    bold=True,
                    underline=True,
                )
            )

            # List entities with Minecraft-style formatting
            for idx, file in enumerate(files_dir, 1):
                file_path = Path(file)
                file_name = file_path.stem.replace("_", " ").title()
                click.echo(
                    click.style(f"#{idx} ", fg="magenta")
                    + click.style(file_name, fg="bright_green", bold=True)
                    + click.style(f" [ {file_path.name} ]", fg="white")
                )

            # Footer
            click.echo(
                "\n"
                + click.style("Found ", fg="bright_white")
                + click.style(str(len(files)), fg="yellow", bold=True)
                + click.style(" awesome entities ready for action!", fg="bright_white")
            )

        except FileNotFoundError:
            click.echo(
                click.style(
                    "\nAlert! Entity workshop directory missing!", fg="red", bold=True
                )
            )
            click.echo(
                click.style("Did you forget to build the castle first?", fg="yellow")
            )
        except Exception as e:
            click.echo(click.style(f"\nCritical Crash! {str(e)}", fg="red", bold=True))
            click.echo(
                click.style("Quick! Call the Minecraft engineers!", fg="bright_red")
            )


@click.command()
@click.option("-m", "--model", is_flag=True)
@click.option("-t", "--texture", is_flag=True)
def listEntity(model: bool, texture: bool):
    list(model=model, texture=texture, object="entity")
    ...


@click.command()
@click.option("-m", "--model", is_flag=True)
@click.option("-t", "--texture", is_flag=True)
def listBlock(model: bool, texture: bool):
    list(model=model, texture=texture, object="blocks")
    ...


def create_metadata():
    """Generate minecorg.json file"""
    
    base_dir = os.getcwd()
    namespace = str(click.prompt("Namespace (e.g., com.yourname)"))
    project_name = str(click.prompt("Project name"))
    metadata = {
        "project": {
            "name":  project_name,
            "description": click.prompt("Project description"),
        },
        "directories": {
            "entity_behavior_folder": str(
                Path(base_dir)/  project_name / "behavior_packs" / namespace / "entities"
            ),
            "entity_resource_folder": str(
                Path(base_dir) / project_name / "resource_packs" / namespace / "entity"
            ),
            "entity_render_controller_folder": str(
                Path(base_dir) /  project_name /"resource_packs" / namespace / "render_controllers"
            ),
            "entity_model_folder": str(
                Path(base_dir) /  project_name /"resource_packs" / namespace / "models" / "entity"
            ),
            "entity_texture_folder": str(
                Path(base_dir) / project_name /"resource_packs" / namespace / "textures" / "entity"
            ),
        },
        "mod": {"name": click.prompt("Mod name"), "namespace": namespace},
    }



    return metadata


def create_env(project_name: str):
    """Generate .env file"""
    env_content = (
        f'PROJECT_NAME="{project_name}"\n'
        'MINECRAFT_PRODUCT="BedrockUWP"\n'
        'CUSTOM_DEPLOYMENT_PATH=""\n'
    )
    env_path = Path(f"{project_name}/.env")
    env_path.write_text(env_content)
    click.echo(f"Created {env_path}")
    ...


def generate_package(project_name:str):
    package = json_handler.import_data_from_json_file_template("package.json")
    package_path = Path(os.getcwd())/ project_name / "package.json"
    with open(package_path, "w") as f:
        json.dump(package, f, indent=2)
    click.echo(f"Created {package_path}")


def generate_just_config(project_name):
    """Generate just.config.ts file."""
    content = script_template.JUST_CONFIG_TEMPLATE.format(project_name=project_name)
    output_file = Path(f"{project_name}/just.config.ts")
    output_file.write_text(content)
    click.echo(f"Created {output_file}")


def generate_eslint_config(project_name):
    content = script_template.ESLINT_CONFIG_TEMPLATE
    output_file = Path(f"{project_name}/eslint.config.mjs")
    output_file.write_text(content)
    click.echo(f"Created {output_file}")


def generate_tf_config(project_name):
    content = script_template.TS_CONFIG_TEMPLATE
    output_file = Path(f"{project_name}/tsconfig.json")
    output_file.write_text(content)
    click.echo(f"Created {output_file}")

    
    