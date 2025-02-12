import click

@click.command()
@click.argument("title")
@click.option("--content", help="Content of the post")
@click.option("--tags", help="Tags for the post (comma-separated)")
@click.option("--version", type=int, default=1, help="Version of the post")
def create(title: str, content: str, tags: str, version: int) -> None:
    """
    A simple CLI to create a post with a title, content, tags, and version.
    """
    # Print the provided inputs
    click.echo(f"Title: {title}")
    click.echo(f"Content: {content}")
    click.echo(f"Tags: {tags}")
    click.echo(f"Version: {version}")

    # Optional: Split tags into a list if provided
    if tags:
        tag_list = tags.split(",")
        click.echo(f"Tags (as list): {tag_list}")

if __name__ == "__main__":
    create()