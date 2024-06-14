import requests

API_URL = 'https://netrix.fun/api'


class Netrix:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_user_info(self, user_id: str):
        headers = {'x-api-key': self.api_key}

        url = API_URL + f'/users/{user_id}'
        response = requests.get(url, headers=headers)

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            print(exc)
            raise

        return response.json()
