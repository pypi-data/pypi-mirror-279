import os
import click

def checkRobocorp():
    #check robocorp installed
    javaStatus = os.popen("rcc --version").read()
    if javaStatus.startswith("v") != True:
        os.popen("""curl -o rcc https://downloads.robocorp.com/rcc/ /latest/linux64/rcc ;
                 chmod a+x rcc ;
                 mv rcc /usr/local/bin/ ;
                 """).read()
        click.secho("robocorp installed successfully", bg='black', fg='green')
