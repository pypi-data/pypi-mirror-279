import subprocess
from typing import IO

def getSubprocessOutput(process: subprocess.Popen[bytes]):

    def log_subprocess_output(pipe: IO[bytes] | None):
        result= ""
        for line in iter(pipe.readline, b''): # b'\n'-separated lines
            a=result + line.decode("utf-8")
            result = a
            
        return result
    
    with process.stdout:
       appiumStatus= log_subprocess_output(process.stdout)
    process.wait() # 0 means success
    
    return appiumStatus