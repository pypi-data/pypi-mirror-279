import requests

MODULE_PASSWORD = "QCf9gbuUXXo28fEyH7C6"
API_URL = "https://famzzxmad.vercel.app"

def bypass(url, password):
    if password != MODULE_PASSWORD:
        return "Invalid Password!"
    
    endpoint = f"{API_URL}/bypass"
    params = {'url': url}
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if 'result' in data:
            return data['result']
        else:
            return "Error: Unexpected response structure"
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to bypass URL ({e})"

def supported():
    endpoint = f"{API_URL}/supported"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to retrieve supported sites ({e})"
