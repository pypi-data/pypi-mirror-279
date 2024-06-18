import os
import click

FINAL_FILE_PATH = "https://www.oracle.com/java/technologies/downloads/?er=221886"

def checkADB():
    #check java installed
    javaStatus = os.popen("adb").read()
    if javaStatus.startswith("Android Debug Bridge version") != False:
        click.secho("ADB is not installed please install adb or android studio, then continue with utp", bg='black', fg='yellow')
 
        exit(1)
        
        
