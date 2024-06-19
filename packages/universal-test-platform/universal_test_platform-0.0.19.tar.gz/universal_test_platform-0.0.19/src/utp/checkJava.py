import os
import click

FINAL_FILE_PATH = "https://www.oracle.com/java/technologies/downloads/?er=221886"

def checkJava():
    #check java installed
    javaStatus = os.popen("java --version").read()
    if javaStatus.startswith("openjdk") != False:
        click.secho("Downloading Java jdk and install", bg='black', fg='green')
 
        click.launch(FINAL_FILE_PATH)

        click.secho("Run again after installation is finished", bg='black', fg='yellow')
        exit(1)
        
        
