# loja/gerencianet_service.py
import hashlib
import json
import time

import requests

from gbstr import settings
from loja.widgets.oauth2_client import get_oauth2_client

class GerencianetService:

    def create_pix_charge( amount, chave_pix, cliente, expiration=3600):

        access_token = get_oauth2_client.get_auth()

        hash_obj = hashlib.sha256((str(time.time())+'pix'+cliente).encode())
        hex_hash = hash_obj.hexdigest()
        txid = hex_hash[:35] if len(hex_hash) >= 35 else hex_hash

        charge_url = settings.URL_GBLACK+f"/v2/cob/{txid}"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        payload = {
            "calendario": {
                "expiracao": expiration
            },
            "devedor": {
                "cpf": "12345678909",
                "nome": "Francisco da Silva"
            },
            "valor": {
                "original": f'{amount}'
            },
            "chave": f'{chave_pix}',
            "solicitacaoPagador": f"Compra do cliente {cliente}"
        }

        response = requests.put(charge_url, json=payload, headers=headers, cert='./homologacao-540691-gblack_store_gerencia_cert.pem')

        if response.status_code == 201:
            data = response.json()
            return data

        else:
            print(f'gerar pix erro : {response.status_code} - {response.text}')

        return 0

    def get_qr_code( txid):
        access_token = get_oauth2_client.get_auth()

        cob_code_url = f'{settings.URL_GBLACK}/v2/cob/{txid}'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(cob_code_url, headers=headers, cert='./homologacao-540691-gblack_store_gerencia_cert.pem')
        resp_pix = response.json()
        id_loc = resp_pix['loc']['id']
        print('resppix  ', resp_pix['loc']['id'])
        qr_code_url = f'{settings.URL_GBLACK}/v2/loc/{id_loc}/qrcode'
        response = requests.get(qr_code_url, headers=headers, cert='./homologacao-540691-gblack_store_gerencia_cert.pem')
        return response.json()
