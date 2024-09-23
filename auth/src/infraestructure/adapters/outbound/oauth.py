import requests
import os

class OAuthProviderFlows:
    def token_validation(self, token: str, provider_url:str):
        response = requests.get(
            provider_url,
            headers={'Authorization': f'Bearer {token}'}
        )
        return response.status_code, response.json
