import requests
import os

class OAuthProviderFlows:
    def token_validation(self, token: str, provider_url:str):
        response = requests.get(
            self.userinfo_endpoint,
            headers={'Authorization': f'Bearer {token}'}
        )
        if response.status_code == 200:
            user_info = response.json()
            return user_info
        return response.status_code
