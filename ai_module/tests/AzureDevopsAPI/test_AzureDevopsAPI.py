from ai_module.src.utils.AzureDevops.AzureDevopsAPI import AzureDevopsAPI
from unittest.mock import Mock, patch, MagicMock
import unittest


class TestAzureDevopsAPI(unittest.TestCase):
    def setUp(self):
        self.pat = "dummypat"
        self.organization = "dummyorganization"
        self.azure_devops_api = AzureDevopsAPI(self.pat, self.organization)

    @patch("ai_module.src.utils.AzureDevops.AzureDevopsAPI.requests.get")
    def test_get_projects_v1(self, mock_requests):
        # Given
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "project1"}, {"name": "project2"}]
        mock_requests.return_value = mock_response

        # When
        projects = self.azure_devops_api.get_projects()

        # Then
        self.assertEqual(projects[0]["name"], "project1")
        self.assertEqual(projects[1]["name"], "project2")

    @patch("ai_module.src.utils.AzureDevops.AzureDevopsAPI.requests.get")
    def test_get_employees_v1(self, mock_requests):
        # Given
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [
                {"id": "00000000-0000-0000-0000-000000000000", "subjectKind": "user"}
            ],
            "count": 1,
            "status_code": 200,
        }
        mock_response.status_code = 200
        mock_requests.return_value = mock_response

        # When
        response = self.azure_devops_api.get_employees()

        # Then
        self.assertEqual(response["count"], 1)
        self.assertEqual(response["status_code"], 200)

    @patch("ai_module.src.utils.AzureDevops.AzureDevopsAPI.requests.get")
    def test_get_work_items_with_ids_v1(self, mock_requests):
        # Given
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "workitem1"}, {"name": "workitem2"}]
        mock_requests.return_value = mock_response

        # When
        work_items = self.azure_devops_api.get_work_items("Project", [1, 2])

        # Then
        self.assertEqual(len(work_items), 2)

    @patch("ai_module.src.utils.AzureDevops.AzureDevopsAPI.requests.get")
    def test_get_work_items_with_no_ids_v1(self, mock_requests):
        # Given
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "workitem1"}, {"name": "workitem2"}]
        mock_requests.return_value = mock_response

        # When
        with self.assertRaises(ValueError):
            work_items = self.azure_devops_api.get_work_items("project1", None)

        # Then
        mock_requests.assert_not_called()

    @patch("ai_module.src.utils.AzureDevops.AzureDevopsAPI.requests.get")
    def test_get_work_items_with_no_project_v1(self, mock_requests):
        # Given
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "workitem1"}, {"name": "workitem2"}]
        mock_requests.return_value = mock_response

        # When
        with self.assertRaises(ValueError):
            work_items = self.azure_devops_api.get_work_items(None, [1, 2])

        # Then
        mock_requests.assert_not_called()


if __name__ == "__main__":
    unittest.main()
