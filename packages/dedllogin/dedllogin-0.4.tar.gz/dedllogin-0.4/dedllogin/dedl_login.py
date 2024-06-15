import requests
import json


class DEDL_auth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_token(self):
        DEDL_TOKEN_URL = 'https://identity.data.destination-earth.eu/auth/realms/dedl/protocol/openid-connect/token'
        DEDL_CLIENT_ID = 'hda-public'
        
        data = { 
            "grant_type": "password", 
            "scope": "openid",
            "client_id": DEDL_CLIENT_ID,
            "username": self.username,
            "password": self.password            
        }

        try:
            response = requests.post(DEDL_TOKEN_URL, data=data)

            if response.status_code == 200: 
                dedl_token = response.json().get("access_token")
                return dedl_token
            else: 
                print(response.json())
                print("Error obtaining DEDL access token") 
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)