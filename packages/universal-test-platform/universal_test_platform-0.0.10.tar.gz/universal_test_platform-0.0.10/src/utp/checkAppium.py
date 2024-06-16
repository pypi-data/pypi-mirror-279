from io import StringIO
import os
import subprocess
from time import sleep
import click

def checkAppium():
    """check appium installed and is running"""

    #check appium is installed
    nodeStatus = os.popen("npm ls --depth 0 -g").read()
    if nodeStatus.count("appium@") <= 0:
        click.secho("Prepare facilitator", bg='black', fg='yellow')
        os.popen("npm install -g appium").read()
        
    def log_subprocess_output(pipe):
        result= ""
        for line in iter(pipe.readline, b''): # b'\n'-separated lines
            a=result + line.decode("utf-8")
            result = a
            
        return result
    
    process = subprocess.Popen(["appium" ,"plugin", "list", "--installed"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with process.stdout:
       appiumStatus= log_subprocess_output(process.stdout)
    process.wait() # 0 means success
    print("appiumStatus",appiumStatus)
    #check device farm is installed
    if appiumStatus.count("device-farm") <= 0:
        click.secho("Prepare local device-farm", bg='black', fg='yellow')
        subprocess.Popen(["appium", "plugin", "install", "--source", "npm", "appium-device-farm"]).wait()
        subprocess.Popen(["appium", "plugin", "install", "--source", "npm", "appium-dashboard"]).wait()
        # os.popen("appium plugin install --source=npm appium-dashboard").read()
        click.secho("Prepared", bg='black', fg='yellow')
    

    handler= subprocess.Popen(["appium", "server", "-ka", "800",  "--use-plugins", "device-farm,appium-dashboard", "-pa", "/wd/hub", "--plugin-device-farm-platform","both"],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                            
    
    sleep(5)
    click.secho("http://127.0.0.1:4723/device-farm", bg='black', fg='green')
    
    return handler