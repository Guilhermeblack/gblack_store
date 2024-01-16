# loja/gerencianet_service.py

import requests
from loja.widgets.oauth2_client import get_oauth2_client

class GerencianetService:


    def create_pix_charge( amount, chave_pix, cliente, expiration=3600):

        access_token = get_oauth2_client.get_auth()

        # Certifique-se de consultar a documentação da Gerencianet para os detalhes completos
        charge_url = 'https://api-pix.gerencianet.com.br/v2/cob'
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
        response = requests.post(charge_url, json=payload, headers=headers)
        return response.json()

    # Adicione métodos para outras operações relacionadas à Gerencianet, se necessário

    def get_qr_code( txid):
        access_token = get_oauth2_client.get_auth()

        # Exemplo: Aqui você faria uma requisição GET para o endpoint que retorna o QR Code
        # Certifique-se de consultar a documentação da Gerencianet para os detalhes completos
        qr_code_url = f'https://api-pix.gerencianet.com.br/v2/loc/{txid}/qrcode'
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(qr_code_url, headers=headers)
        return response.json()