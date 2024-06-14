import requests
import json

def hda_access(username, password, token_url='https://identity.data.destination-earth.eu/auth/realms/dedl/protocol/openid-connect/token'):
    username = username
    password = password
    access_token_response = requests.post(
        token_url,
        data = {'grant_type': 'password','scope' : 'openid', 'client_id' : 'hda-public', 'username' : username, 'password' : password},
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
    )
    return access_token_response.json()['access_token']