import requests
import base64
import urllib.parse
from typing import List, Optional


# makes HTTP requests to Azure DevOps
class AzureDevopsAPI:
    auth: str
    instance: str
    organization: str
    headers: dict
    url_preamble: str

    def _run_request(self, endpoint: str, headers: dict, data: dict = None) -> dict:
        if not data:
            request = requests.get(endpoint, headers=headers)
        else:
            request = requests.post(endpoint, headers=headers, json=data)
        request.raise_for_status()
        return request.json()

    def __init__(self, auth: str, organization: str):
        encoded_token = str(base64.b64encode(bytes(":" + auth, "ascii")), "ascii")
        self.auth = encoded_token
        self.organization = organization
        self.url_preamble = f"https://dev.azure.com/{self.organization}"
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + self.auth,
        }

    def get_projects(self) -> dict:
        endpoint_posfix = "/_apis/projects?api-version=7.0"
        endpoint = self.url_preamble + endpoint_posfix
        return self._run_request(endpoint, self.headers)

    def get_project_info(self, projectId: str) -> dict:
        endpoint_posfix = (
            "/{self.organization}/_apis/projects/{projectId}?api-version=7.0"
        )
        endpoint = self.url_preamble + endpoint_posfix
        return self._run_request(endpoint, self.headers, None)

    def get_employees(self) -> dict:
        endpoint = f"https://vssps.dev.azure.com/{self.organization}/_apis/graph/users?api-version=7.0-preview"
        return self._run_request(endpoint, self.headers)

    def get_work_items(self, project: str, ids: List[int], as_of: str = None) -> dict:
        if not project:
            raise ValueError("project must be provided")
        if not ids:
            raise ValueError("ids must be provided")
        project = urllib.parse.quote(project)
        ids = "ids=" + ",".join([str(id) for id in ids]) if ids else ""
        as_of = "&asOf=" + urllib.parse.quote(as_of) if as_of else ""
        endpoint = (
            f"{self.url_preamble}/{project}/_apis/wit/workitems?{ids}&api-version=7.0"
        )
        return self._run_request(endpoint, self.headers)

    def get_work_item(self, project: str, id: int) -> dict:
        project = urllib.parse.quote(project)
        url = f"{self.url_preamble}/{project}/_apis/wit/workitems/{id}?api-version=7.0"
        return self._run_request(url, self.headers)

    def create_work_item(
        self,
        project: str,
        title: str,
        type: str,
        description: Optional[str] = None,
        assignedMail: Optional[str] = None,
    ) -> dict:
        endpoint = (
            f"{self.url_preamble}/{project}/_apis/wit/workitems/${type}?api-version=7.0"
        )
        payload = self._make_workitem_payload(title, description, assignedMail)
        headers = {
            "Content-Type": "application/json-patch+json",
            "Authorization": self.headers["Authorization"],
        }
        return self._run_request(endpoint, headers, payload)

    def update_work_item(
        self,
        id: int,
        project: str,
        title: str = None,
        description: str = None,
        assignedMail: str = None,
    ) -> dict:
        url = "https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0"
        url = url.format(organization=self.organization, project=project, id=id)
        payload = self._make_workitem_payload(title, description, assignedMail)

        headers = self.headers
        headers["Content-Type"] = "application/json-patch+json"

        request = requests.patch(url, headers=headers, json=payload)

        print(request.json())
        request.raise_for_status()

        return request.json()

    def _check_workitem_type(self, type: str):
        types = {
            "Epic",
            "Feature",
            "UserStory",
            "Product Backlog Item",
            "Requirement",
            "Task",
            "Bug",
            "Issue",
            "Impediment",
            "TestPlan",
            "TestSuite",
            "TestCase",
        }
        if type not in types:
            raise (ValueError("Invalid work item type: " + type))

    def _make_workitem_payload(
        self,
        title: str,
        description: Optional[str] = None,
        assignedMail: Optional[str] = None,
    ) -> object:
        payload = []
        if title:
            payload.append(
                {
                    "op": "add",
                    "path": "/fields/System.Title",
                    "value": title,
                }
            )
        if description:
            payload.append(
                {
                    "op": "add",
                    "path": "/fields/System.Description",
                    "value": description,
                }
            )
        if assignedMail:
            payload.append(
                {
                    "op": "add",
                    "path": "/fields/System.AssignedTo",
                    "value": assignedMail,
                }
            )
        return payload
