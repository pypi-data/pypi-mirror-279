import socket
# from robot.libraries.BuiltIn import BuiltIn
 
class utp():
    def __init__(self):
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
