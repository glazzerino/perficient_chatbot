import sys

sys.path.append("ai_module/src")
from utils.Notion.NotionAPI import NotionAPI
from env import NotionCredentials
from utils.Notion.page_schema import Page


class NotionWrapper:
    def __init__(self):
        self.token = NotionCredentials.token
        self.db_id = NotionCredentials.database_id
        self.notionAPI = NotionAPI(token=self.token, database_id=self.db_id)

    def create_page(self, title: str, content: str) -> dict:
        page = Page().set_database_id(self.db_id)
        page.with_title(title).with_paragraph(content)
        return self.notionAPI.create_page(page)
