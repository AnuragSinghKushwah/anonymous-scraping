from requests import get

def get_public_ip():
    "Function to get public ip address of the system"
    ip = get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))
    return ip