import click
import time
import subprocess
from utp.checkADB import checkADB
from utp.checkAppium import checkAppium
from utp.checkJava import checkJava
from utp.checkNode import checkNode
from utp.checkRobocorp import checkRobocorp
from utp.checkRobotFramework import checkRobotFramework
from utp.clearArtifact import clearArtifact
from utp.localHub import runLocalHub
from utp.checkport import isPortUsed


@click.group()
def cli():
    pass

@click.command()
# @click.option('--name', prompt='Identify youself by name')
def web():
    """Run test cases locally"""

    #check node installed
    checkNode()

    checkJava()
    
    localHubIsRunning = isPortUsed(4444)
    hubHandler= None
    if localHubIsRunning == False:
        click.secho("running Hub Locally")
        hubHandler = runLocalHub()
        time.sleep(10)
        click.secho("Start Hub and Node standalone", bg='black', fg='green')

    checkRobotFramework()

    checkRobocorp()

    clearArtifact()

    subprocess.Popen(["rcc", "run", "--task", "Web"]).wait()
    
    if hubHandler is not None:
        hubHandler.kill()
    
        


@click.command()
# @click.option('--name', prompt='Identify youself by name')
def app():
    """Run test cases locally"""

    #check node installed
    checkNode()
    
    checkADB()

    appiumHandler = checkAppium()
        
    checkRobotFramework()

    checkRobocorp()

    clearArtifact()

    subprocess.Popen(["rcc", "run", "--task", "App"]).wait()
    if appiumHandler is not None:
        appiumHandler.kill()
    

# @click.command()
# @click.Choice()
cli.add_command(web)
cli.add_command(app)

if __name__ == '__main__':
    cli()