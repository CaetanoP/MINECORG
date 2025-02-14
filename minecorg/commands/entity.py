import click
from pathlib import Path
from ..utils import file_utils
from . import project
from ..classes import entity as e
import json
from rich.console import Console
from rich.table import Table
from ..utils import json_handler

console = Console()


@click.command()
def create():
    """
    Create a new entity.
    """
    console.rule("[bold blue]Entity Creation[/bold blue]")
    console.print("[bold green]Welcome to the Entity Creation Wizard![/bold green]")
    console.print(
        "[bold green]Follow the steps to create a new entity for your project.[/bold green]\n\n"
    )
    console.print("[bold yellow]Step 1:[/bold yellow] Enter the name of the entity.\n")

    ## Take Name
    name = console.input("[bold blue]Name: [/bold blue]")

    ## Verify Name
    if name is (None or ""):
        console.print("[bold red]\nError!\nEmpty name is not allowed")
        raise click.Abort()

    ## Creating entity with the input name
    entity = e.Entity(name.lower().replace(" ", "_"))

    ## Request the Model
    console.print("\n[bold yellow]Step 2:[/bold yellow] Add entity model file.\n")
    model_root = Path(f"{project.PROJECT_DIRECTORY}/resource_packs/models/entity")
    model_file_name = file_utils.file_request(model_root, "model file")
    entity_model_request(entity=entity, folder=model_root, file_name=model_file_name)

    ## Request the Texture
    console.print("\n[bold yellow]Step 3:[/bold yellow] Add entity texture file.\n")
    texture_root = Path(f"{project.PROJECT_DIRECTORY}/resource_packs/textures/entity")
    texture_file_name = file_utils.file_request(texture_root, "texture file")
    entity_texture_request(
        entity=entity, folder=texture_root, file_name=texture_file_name
    )

    ## Create the RenderController
    console.print(
        "\n[bold yellow]Step 4:[/bold yellow] Creating entity render controller.\n"
    )
    entity_render_control(entity)
    ## Create the Entity RP
    console.print(
        "\n[bold yellow]Step 5:[/bold yellow] Creating entity resource pack file.\n"
    )
    entity_resource_pack(entity=entity)

    ## Create the Entity BP
    console.print(
        "\n[bold yellow]Step 6:[/bold yellow] Creating entity behavior pack file.\n"
    )
    entity_behavior_pack(entity)
    click.echo("Entity Created")


def entity_behavior_pack(entity: e.Entity):
    entity_behavior_pack = Path(
        f"{project.PROJECT_DIRECTORY}/behavior_packs/entities/{entity.name}.json"
    )

    # import data
    entity_data = json_handler.import_data_from_json_file_template("entity.json")
    old_values = ["namespace:entity_name"]
    new_values = [f"{project.NAMESPACE}:{entity.name}"]
    entity_data = json_handler.rename_values_from_json_data(
        entity_data, old_values=old_values, new_values=new_values
    )
    with open(entity_behavior_pack, "w") as file:
        json.dump(entity_data, file, indent=2)
    console.print(
        f"[bold green]Behavior created at:[/bold green][bold white]{entity_behavior_pack}[/bold white]"
    )

def entity_resource_pack(entity: e.Entity):
    entity_resource_path = Path(
        f"{project.PROJECT_DIRECTORY}/resource_packs/entity/{entity.name}.entity.json"
    )
    # import data
    entity_data = json_handler.import_data_from_json_file_template("entity.entity.json")
    if entity_data == {}:
        raise click.Abort()
    old_values = [
        "namespace:entity_name",
        "textures/entity/entity_name",
        "geometry.entity_name",
        "animation.entity_name.idle",
        "controller.animation.entity_name.general",
        "controller.render.entity_name",
    ]
    new_values = [
        f"{project.NAMESPACE}:{entity.name}",
        f"textures/entity/{entity.name}",
        f"geometry.{entity.name}",
        f"animation.{entity.name}.idle",
        f"controller.animation.{entity.name}.general",
        f"controller.render.{entity.name}",
    ]

    entity_data = json_handler.rename_values_from_json_data(
        entity_data, old_values=old_values, new_values=new_values
    )
    with open(entity_resource_path, "w") as file:
        json.dump(entity_data, file, indent=2)
    console.print(
        f"[bold green]Resource created at:[/bold green][bold white]{entity_resource_path}[/bold white]"
    )

def entity_render_control(entity: e.Entity):
    """
    Create a render controller JSON file for the given entity.

    Args:
        entity (e.Entity): The entity for which the render controller is being created.
    """
    try:
        # Define the path for the new render controller file
        render_controller_path = Path(
            f"{project.PROJECT_DIRECTORY}/resource_packs/render_controllers/{entity.name}.render_controller.json"
        )

        # Load the template data for the render controller
        render_controller_data = json_handler.import_data_from_json_file_template(
            "entity.render_controllers.json"
        )

        # Rename the key in the template data to match the entity name
        render_controller_data = json_handler.rename_key_from_json_data(
            render_controller_data,
            "controller.render.unknown",
            f"controller.render.{entity.name}",
        )

        # Write the updated data to the new render controller file
        with open(render_controller_path, "w") as file:
            json.dump(render_controller_data, file, indent=2)
        console.print(
            f"[bold green]Render controller created at:[/bold green][bold white]{render_controller_path}[/bold white]"
        )
    except FileNotFoundError:
        console.print("[bold red]Error: Template file not found.[/bold red]")
        raise click.Abort()
    except json.JSONDecodeError:
        console.print(
            "[bold red]Error: Failed to decode JSON from the template file.[/bold red]"
        )
        raise click.Abort()
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")
        raise click.Abort()

def entity_texture_request(entity: e.Entity, folder: Path, file_name: str):
    """
    Handles the request to update the texture file name for a given entity.
    Args:
        entity (e.Entity): The entity for which the texture file name needs to be updated.
        folder (Path): The folder where the texture file is located.
        file_name (str): The current name of the texture file.
    Returns:
        None
    """
    ## Taking the file path
    file_path = folder / file_name
    ## Changing the file name
    update_file_name(file_path, f"{entity.name}.png")

def entity_model_request(entity: e.Entity, folder: Path, file_name: str):
    ## Taking the file path
    file_path = folder / file_name
    ##
    update_geo_json_identifier_component(file_path=file_path, entity_name=entity.name)
    update_file_name(file_path, f"{entity.name}.geo.json")
    console.print(f"file_name add: {file_name}")


def update_geo_json_identifier_component(file_path: Path, entity_name: str):
    """
    Update the 'identifier' field in the .geo.json file to match the entity name.

    Args:
        file_path (Path): Path to the .geo.json file.
        entity_name (str): Name of the entity to set as the identifier.
    """
    try:
        # Load the JSON file
        with open(file_path, "r") as file:
            data = json.load(file)

        identifier_update = False
        # Update the identifier
        for geometry in data.get("minecraft:geometry", []):
            if "description" in geometry and "identifier" in geometry["description"]:
                geometry["description"]["identifier"] = f"geometry.{entity_name}"
                identifier_update = True
        if not identifier_update:
            console.print("[bold red]Json file structure not recognized[/bold red]")
            raise click.Abort()

        # Save the updated JSON back to the file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

        console.print(
            f"\n[bold blue]Updated identifier to: [/bold blue][bold white]geometry.{entity_name}[/bold white]"
        )
    except Exception as e:
        console.print(
            f"\n[bold red]Error updating identifier: {e}\nMake sure that the json file has an identifier component inside of description[/bold red]"
        )
        raise click.Abort()


def update_file_name(file_path: Path, new_name: str):
    """
    Renames a file to a new name if it exists.
    Args:
        file_path (Path): The path to the file to be renamed.
        new_name (str): The new name for the file.
    Raises:
        click.Abort: If the file does not exist, if there is a permission error,
        or if any other unexpected error occurs.
    """

    old_name = file_path.name
    try:
        if file_path.exists():
            new_file_path = file_path.with_name(new_name)
            file_path.rename(new_file_path)
            console.print(
                f"[bold blue]Renamed file[/bold blue] to:[bold white] {new_file_path.name}[/bold white]  "
            )
        else:
            console.print("[bold red]Error: Added file not found.[/bold red]")
            raise click.Abort()
    except FileNotFoundError:
        console.print(f"[bold red]Error: File {old_name} not found.[/bold red]")
        raise click.Abort()
    except PermissionError:
        console.print(
            f"[bold red]Error: Permission denied while renaming {old_name}.[/bold red]"
        )
        raise click.Abort()
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")
        raise click.Abort()


@click.command()
@click.option("--entity", is_flag=True)
def list(
    entity: bool,
):
    """
    List all entities
    """
    try:
        entities_dir = (
            Path(project.PROJECT_DIRECTORY)
            / "behavior_packs"
            / "dant_myal"
            / "entities"
        )
        click.echo(click.style("Scanning entity vault...", fg="yellow", bold=True))

        files = file_utils.find_files(entities_dir)

        if not files:
            click.echo(
                click.style("\nWhoops! No entities found in the workshop!", fg="red")
            )
            return

        # Header
        click.echo(
            "\n"
            + click.style(
                "Available Entities ({}):".format(len(files)),
                fg="cyan",
                bold=True,
                underline=True,
            )
        )

        # List entities with Minecraft-style formatting
        for idx, file in enumerate(files, 1):
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
