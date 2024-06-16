import subprocess
import os

def runLocalHub():
      handler= subprocess.Popen(["java", "-jar", os.path.dirname(__file__) + "/../setup/selenium-server-4.21.0.jar","standalone"],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
      return handler
    
