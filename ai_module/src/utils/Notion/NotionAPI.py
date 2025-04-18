import requests
from .page_schema import Page


class NotionAuth:
    token: str
    database_id: str


class NotionAPI:
    headers: dict
    auth: NotionAuth
    base_url = "https://api.notion.com"
    params = {
        "parent": {
            "database_id": str,
        }
    }

    def __init__(self, token: str, database_id: str):
        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.database_id = database_id

    def create_page(self, page: Page):
        url = self.base_url + "/v1/pages"
        page.set_database_id(self.database_id)
        response = requests.post(url, headers=self.headers, json=page.data)
        print(response.content)
        return response
