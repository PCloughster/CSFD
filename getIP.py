import requests

def getExternalIP():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return False
    except Exception as e:
       return False