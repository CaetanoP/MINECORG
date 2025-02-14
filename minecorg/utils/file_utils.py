
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
import click
console = Console()

def find_file(folder_path:Path, file_name:str):
    """
    Searches for a file with the specified name within a given folder path and its subdirectories.
    Args:
        folder_path (Path): The path to the folder where the search should begin.
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



def file_request(folder: Path, msg: str) -> str:
    """
    Prompts the user to add a new file to the specified folder and returns the name of the newly added file.
    This function performs the following steps:
    1. Checks if the specified folder exists. If not, it prints an error message and aborts the operation.
    2. Captures the current set of files in the folder.
    3. Prompts the user to add a new file to the folder and waits for user confirmation.
    4. Captures the new set of files in the folder.
    5. Determines the difference between the old and new sets of files to identify the newly added file.
    6. If no new files are detected or multiple new files are detected, it prints an error message and aborts the operation.
    7. Returns the name of the newly added file.
    Args:
        folder (Path): The path to the folder where the new file should be added.
        msg (str): A message describing the type of file to be added.
    Returns:
        str: The name of the newly added file.
    Raises:
        click.Abort: If the folder does not exist, no new files are detected, or multiple new files are detected.
    """
    if not folder.exists():
        console.print(
            f"\n[bold red]Error![/bold red]\n[bright_white][bold blue]Folder not found:[/bold blue] {folder}[/bright_white]"
        )
        console.print(
            "\n[bold purple]Hint: Use 'minecorg scan' to identify missing folders/files[bold purple]"
        )
        raise click.Abort()

    old_files = set(find_files(folder))
    console.print(
        f"[bold blue]Add the {msg} in: [/bold blue][underline bright_white]{folder}[/underline bright_white]"
    )
    console.input(
        f"[bold green]Press Enter to continue once the {msg} is added...[/bold green]"
    )
    new_files = set(find_files(folder))

    files = old_files ^ new_files

    if not files:
        console.print("[bold red]Error: No new files detected.[/bold red]")
        raise click.Abort()
    if len(files) > 1:
        console.print(
            "[bold red]Error: Multiple new files detected. Only add one.[/bold red]\n"
        )
        table = Table(title="Detected Files")
        table.add_column("File Name", style="cyan", no_wrap=True)
        for file in files:
            table.add_row(str(file))
        console.print(table)
        raise click.Abort()

    return files.pop()

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