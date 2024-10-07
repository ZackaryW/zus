import click
from ..core.caching import GitCacher

clickgroup = click.Group(name="zuucache", help="Caching commands")

@clickgroup.command(name="add", help="Add a new git repository to the cache")
@click.argument("giturl")
@click.option("--branch", default=None, help="Branch to checkout")
@click.option("--expire", default=24 * 60 * 60, help="Expiration time in seconds")
def add(giturl, branch, expire):
    cacher = GitCacher()
    cacher.add(giturl, branch, expire)
    click.echo(
        f"Added {giturl} to cache with branch {branch} and expiration {expire} seconds"
    )


@clickgroup.command(name="get", help="Get a file from the cache")
@click.argument("path")
@click.option("--usr", default=None, help="User of the repository")
@click.option("--name", default=None, help="Name of the repository")
@click.option("--branch", default=None, help="Branch of the repository")
@click.option("--fuzzy", is_flag=True, help="Enable fuzzy matching")
def get(path, usr, name, branch, fuzzy):
    cacher = GitCacher()
    cached_path = cacher.get(path, usr, name, branch, fuzzy)
    if cached_path:
        click.echo(f"File found at: {cached_path}")
    else:
        click.echo("File not found in cache")


@clickgroup.command(name="expired", help="Check for expired cache entries")
@click.option("--name", default=None, help="Name of the repository")
@click.option("--usr", default=None, help="User of the repository")
@click.option("--branch", default=None, help="Branch of the repository")
def check_expired(name, usr, branch):
    cacher = GitCacher()
    cacher.check_expired(name, usr, branch)
    click.echo("Checked for expired cache entries")

if __name__ == "__main__":
    clickgroup()