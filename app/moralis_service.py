import requests

class MoralisService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://deep-index.moralis.io/api/v2'

    def get_wallet_info(self, address):
        url = f'{self.base_url}/{address}/balance'
        headers = {
            'X-API-Key': self.api_key,
            'accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_wallet_transactions(self, address, chain='eth'):
        url = f'{self.base_url}/{address}/transactions'  # Корректный URL
        headers = {
            'X-API-Key': self.api_key,
            'accept': 'application/json'
        }
        params = {
            'chain': chain
        }
        response = requests.get(url, headers=headers, params=params)

        # Логируем ответ API для отладки
        print(f"Ответ API: {response.text}")

        if response.status_code != 200:
            print(f"Ошибка запроса к Moralis API: {response.status_code}")
            return []

        try:
            data = response.json()
            return data['result']  # Moralis возвращает транзакции в поле 'result'
        except (requests.exceptions.JSONDecodeError, KeyError) as e:
            print(f"Ошибка при обработке ответа API: {e}")
            return []

    def get_wallet_assets(self, address):
        url = f'{self.base_url}/{address}/erc20'
        headers = {
            'X-API-Key': self.api_key,
            'accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.json()
