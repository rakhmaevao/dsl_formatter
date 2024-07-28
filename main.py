from pathlib import Path
import click

from src.app import App


@click.command()
@click.option("--verbose", "-v", is_flag=True, default=False)
@click.argument('path')
def main(path, verbose):
    App().run(Path(path), verbose=verbose)

if __name__ == '__main__':
    main()