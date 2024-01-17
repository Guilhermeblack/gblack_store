# loja/gerencianet_service.py

import requests

from gbstr import settings
from loja.widgets.oauth2_client import get_oauth2_client

class GerencianetService:

    def create_pix_charge( amount, chave_pix, cliente, expiration=3600):

        access_token = get_oauth2_client.get_auth()
        print('tkn  ', access_token)

        # Certifique-se de consultar a documentação da Gerencianet para os detalhes completos
        charge_url = settings.URL_GBLACK+'/v2/cob'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'calendario': {'expiracao': expiration},
            'valor': {'original': str(amount)},
            'chave': chave_pix,
            'solicitacaoPagador': f'Compra do cliente {cliente}',
        }
        response = requests.post(charge_url, json=payload, headers=headers, cert=('./homologacao-540691-gblack_store_gerencia_cert.pem', ''))
        return response.json()

    def get_qr_code( txid):
        access_token = get_oauth2_client.get_auth()

        qr_code_url = f'{settings.URL_GBLACK}/v2/loc/{txid}/qrcode'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(qr_code_url, headers=headers, cert=('./homologacao-540691-gblack_store_gerencia_cert.pem', ''))
        return response.json()