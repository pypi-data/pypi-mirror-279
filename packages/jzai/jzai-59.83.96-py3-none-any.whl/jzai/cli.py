import click
from .bot import main

@click.command()
def run():
    """Run the bot."""
    main()

if __name__ == '__main__':
    run()
    