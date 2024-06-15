import requests

MODULE_PASSWORD = "QCf9gbuUXXo28fEyH7C6"

def bypass(url, password):
    if password != MODULE_PASSWORD:
        return "Invalid Password!"
    
    api_url = "https://famzzxmad.vercel.app/bypass"
    params = {'url': url}
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'result' in data:
            return data['result']
        else:
            return "Error: Unexpected response structure"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def supported():
    api_url = "https://famzzxmad.vercel.app/supported"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
