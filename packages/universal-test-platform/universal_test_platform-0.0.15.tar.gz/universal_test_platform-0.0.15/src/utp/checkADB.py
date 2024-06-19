import subprocess
import click

from utp.utils import getSubprocessOutput


def checkADB():
    #check java installed
    process = subprocess.Popen(["adb"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    javaStatus =  getSubprocessOutput(process)
    
    if javaStatus.count("Android Debug Bridge version") <= 0:
        click.secho("ADB is not installed please install adb or android studio, then continue with utp", bg='black', fg='yellow')
 
        exit(1)
        
        
