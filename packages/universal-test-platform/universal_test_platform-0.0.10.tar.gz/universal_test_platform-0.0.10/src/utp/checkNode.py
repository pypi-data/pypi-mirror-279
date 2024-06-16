import os

import click


def checkNode():
    """check node installed"""
    nodeStatus = os.popen("node -v").read()
    if nodeStatus.startswith("v") != True:
        click.secho("Nodejs is not installed please install it", bg='black', fg='red')
        raise Exception("Node js is not installed")
