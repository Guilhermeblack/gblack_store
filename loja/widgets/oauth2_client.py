import requests
import os
import base64
from datetime import datetime, timedelta
from gbstr.settings import CLIENT_SECRET_GBLACK, CLIENT_ID_GBLACK, URL_GBLACK

class OAuth2Client:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_type = None
        self.expires_at = None
        self.cert = './homologacao-540691-gblack_store_gerencia_cert.pem'

    def authenticate_token(self):

        payload = "{\r\n    \"grant_type\": \"client_credentials\"\r\n}"

        auth = base64.b64encode((f"{self.client_id}:{self.client_secret}").encode()).decode()
        headers = {
            'Authorization': f"Basic {auth}",
            'Content-Type': 'application/json'
        }

        response = requests.post(self.token_url + '/oauth/token', data=payload, cert=self.cert, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.token_type = data['token_type']
            self.expires_at = datetime.now() + timedelta(seconds=data['expires_in'])

        else:
            print(f'Erro na autenticação: {response.status_code} - {response.text}')


    def get_auth(self):

        if self.expires_at is None or self.expires_at < datetime.now():
            self.authenticate_token()

        return self.access_token


# Exemplo de uso:
get_oauth2_client = OAuth2Client(
    token_url=URL_GBLACK,
    client_id=CLIENT_ID_GBLACK,
    client_secret=CLIENT_SECRET_GBLACK
)

# oauth2_client.get_auth()

