from . import app
from .gitea import app as gitea_app
from .k8s import app as k8s_app
from .smb import app as smb_app

app.add_typer(gitea_app, name='gitea')
app.add_typer(k8s_app, name='k8s')
app.add_typer(smb_app, name='smb')


def main():
    app()
