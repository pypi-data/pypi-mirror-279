import os


def appVariables(androidApp: str, androidPlatformVersion: str):
    my_env = os.environ
    my_env["ANDROID_AUTOMATION_NAME"] = 'UIAutomator2'
    my_env["ANDROID_APP"] = androidApp or 'http://172.20.74.25:4723/device-farm/apps/file-1717336325068.apk'
    my_env["ANDROID_PLATFORM_NAME"] = 'Android'
    my_env["ANDROID_PLATFORM_VERSION"] = androidPlatformVersion or '11'
    
    return my_env
    