import click
from twitcomp.models import DB

def create_db():
    """Creates database"""
    DB.create_all()
    
def drop_db():
    """Cleans database"""
    DB.drop_all()

def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))
