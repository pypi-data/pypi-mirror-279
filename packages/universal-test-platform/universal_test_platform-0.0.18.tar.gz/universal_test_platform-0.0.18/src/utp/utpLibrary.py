import os
import socket
from robot.libraries.BuiltIn import BuiltIn
from AppiumLibrary import AppiumLibrary

class utp():
    def __init__(self):
        self.appium = AppiumLibrary()
        pass
    
    def get_hub_url(self):

        try:
            # Create a socket and connect to an external server to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 53))  # Connect to Google's DNS server
            ip = s.getsockname()[0]
            s.close()
        except Exception as e:
            ip = '127.0.0.1'  # Default to localhost in case of an error
            print(f"Error obtaining IP address: {e}")
        
        return ip

    def open_android_application(self):
        ip = self.get_hub_url()
        
        ANDROID_AUTOMATION_NAME = os.environ["ANDROID_AUTOMATION_NAME"] or 'UIAutomator2'
        ANDROID_APP = os.environ["ANDROID_APP"] or 'device-farm/apps/file-1717336325068.apk'
        ANDROID_PLATFORM_NAME = os.environ["ANDROID_PLATFORM_NAME"] or 'Android'
        ANDROID_PLATFORM_VERSION = os.environ["ANDROID_PLATFORM_VERSION"] or '11'
        
        remote_url = f'http://{ip}:4723/wd/hub'
        app_url = f'http://{ip}:4723/{ANDROID_APP}'
        
        self.appium.open_application(
            remote_url,
            automationName=ANDROID_AUTOMATION_NAME,
            platformName=ANDROID_PLATFORM_NAME,
            platformVersion=ANDROID_PLATFORM_VERSION,
            app=app_url,
            appPackage='com.digikala',
            appWaitActivity='*'
        )
        BuiltIn().sleep('5s')
        
        
        