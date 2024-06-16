import click
import time
import os
import subprocess
import sys
from checkAppium import checkAppium
from checkNode import checkNode
from clearArtifact import clearArtifact
from localHub import runLocalHub
from checkport import isPortUsed


@click.group()
def cli():
    pass


@click.command()
# @click.option('--name', prompt='Identify youself by name')
def web():
    """Run test cases locally"""

    #check node installed
    checkNode()

    #check java installed
    javaStatus = os.popen("java --version").read()
    if javaStatus.startswith("openjdk") != True:
        click.secho("Java jdk is not installed please install it", bg='black', fg='red')

        
    localHubIsRunning = isPortUsed(4444)
    hubHandler= None
    if localHubIsRunning == False:
        click.secho("running Hub Locally")
        hubHandler = runLocalHub()
        time.sleep(10)
        click.secho("Start Hub and Node standalone", bg='black', fg='green')
    
    #check robotframework installed
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    if installed_packages.count("robotframework") <= 0:
        subprocess.check_output([sys.executable, '-m', 'pip', 'install', 'robotframework'])
        click.secho("robotframework installed successfully", bg='black', fg='green')

    #check robocorp installed
    javaStatus = os.popen("rcc --version").read()
    if javaStatus.startswith("v") != True:
        os.popen("""curl -o rcc https://downloads.robocorp.com/rcc/ /latest/linux64/rcc ;
                 chmod a+x rcc ;
                 mv rcc /usr/local/bin/ ;
                 """).read()
        click.secho("robocorp installed successfully", bg='black', fg='green')

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

    appiumHandler = checkAppium()
        
    #check robotframework installed
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    if installed_packages.count("robotframework") <= 0:
        subprocess.check_output([sys.executable, '-m', 'pip', 'install', 'robotframework'])
        click.secho("robotframework installed successfully", bg='black', fg='green')

    #check robocorp installed
    javaStatus = os.popen("rcc --version").read()
    if javaStatus.startswith("v") != True:
        os.popen("""curl -o rcc https://downloads.robocorp.com/rcc/ /latest/linux64/rcc ;
                 chmod a+x rcc ;
                 mv rcc /usr/local/bin/ ;
                 """).read()
        click.secho("robocorp installed successfully", bg='black', fg='green')

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