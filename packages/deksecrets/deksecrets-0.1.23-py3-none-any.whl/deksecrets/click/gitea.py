import sys
import typer
from typing import List
from getpass import getpass
from dektools.shell import output_data
from ..tools.gitea import GiteaManager

app = typer.Typer(add_completion=False)

default_name = 'default'


@app.command()
def login(url, token=None, name=default_name):
    if not token:
        token = getpass('Please input token:')
    GiteaManager(name).login(url, token)


@app.command()
def logout(name=default_name):
    GiteaManager(name).logout()


@app.command()
def init(name=default_name):
    sys.stdout.write(GiteaManager(name).init())


@app.command()
def upload(name=default_name):
    GiteaManager(name).upload()


@app.command()
def fetch(org_project_tag_environment, path=None, out=None, fmt=None, prefix=None, name=default_name):
    org, project, tag, environment = org_project_tag_environment.split('/')
    data = GiteaManager(name).fetch(org, project, tag, environment, path)
    output_data(data, out, fmt, prefix)


@app.command()
def clone(orgs: List[str], name=default_name):
    GiteaManager(name).fetch_all(orgs)
