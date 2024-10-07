
import click

from .eagle import new_ver4_library

clickgroup = click.Group(name="eagle", help="Eagle File Explorer commands")

@clickgroup.command()
@click.argument('path')
def newlib(path):
    click.echo(f"creating eagle library at {path}")
    new_ver4_library(path)


if __name__ == "__main__":
    clickgroup()

