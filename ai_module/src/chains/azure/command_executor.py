from ai_module.src.llm_tools.AzureDevopsAPI_Tool import azure_devops_cli
import json


class CommandExecutor:
    output: str = "Empty"

    def execute(self, command: str, token: str, org: str):
        try:
            self.output = json.dumps(azure_devops_cli(command, token, org))
        except Exception as e:
            self.output = "ERROR: " + str(e)
        return self

    def get_output(self):
        return self.output
