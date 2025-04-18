class Page:
    data: dict
    database_id: str

    def __init__(self):
        self.data = {
            "properties": {},
            "children": [],
        }

    def set_database_id(self, database_id: str):
        self.data["parent"] = {"database_id": database_id}
        return self

    def with_title(self, title: str):
        self.data["properties"]["Name"] = {"title": [{"text": {"content": title}}]}
        return self

    def _get_paragraph_dict(self, paragraph: str) -> dict:
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": paragraph}}]
            },
        }

    def with_paragraph(self, paragraph: str):
        self.data["children"].append(self._get_paragraph_dict(paragraph))
        return self

    def __str__(self):
        return self.data.__str__()
