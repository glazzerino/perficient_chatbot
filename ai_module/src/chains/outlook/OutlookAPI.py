import requests
import base64
import urllib.parse
from typing import List

# makes HTTP requests to Outlook
class OutlookAPI:
    def __init__(self, auth: str):
        encoded_token = str(base64.b64encode(
            bytes(':'+auth, 'ascii')), 'ascii')
        self.auth = encoded_token
        self.url_preamble = "https://graph.microsoft.com/v1.0"
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {auth}'
        }

    def get_inbox_messages():
        # we can make it more detailed later
        # endpoint_postfix = "/me/mailfolders/inbox/messages?$select=subject,from,receivedDateTime&$top=25&$orderby=receivedDateTime%20DESC"
        endpoint_postfix = "/me/mailfolders/inbox/messages"
        endpoint = self.url_preamble + endpoint_postfix
        print("url: " + endpoint)
        request = requests.get(endpoint, headers=self.headers)
        request.raise_for_status()
        return request.json()