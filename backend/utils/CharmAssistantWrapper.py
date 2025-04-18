from ai_module.src.chains.azure.base import AzureDevopsChain
from backend.utils.AssisantWrapperInterface import AssistantWrapperInterface
from langchain.agents import Tool
from langchain.llms import OpenAI
import streamlit as st
from streamlit_chat import message
from ai_module.src.chains.notion.base import NotionChain
from langchain.agents import load_tools, Agent
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.schema import messages_from_dict


# This class handles the interaction with the underlying AI module logic
class CharmAssistantWrapper(AssistantWrapperInterface):
    def run_prompt(self, prompt: str, context: dict, auth: dict) -> str:
        agent = self._get_agent(auth, context["history"])
        response = agent.run(prompt)
        return response

    def _get_agent(self, auth: dict, history: dict) -> Agent:
        self.llm = OpenAI(temperature=0.0, model_name="text-davinci-003")

        self.planner = load_chat_planner(self.llm)
        tools = self.get_tools(auth)
        self.executor = load_agent_executor(self.llm, tools, verbose=True)
        agent = PlanAndExecute(
            planner=self.planner,
            executer=self.executor,
            verbose=True,
        )
        return agent

    def get_tools(self, auth: dict) -> list[Tool]:
        azure_tool = self._get_azure_tool(auth)
        notion_tool = self._get_notion_tool(auth)
        return [azure_tool, notion_tool]

    def _get_azure_tool(self, auth: dict):
        return Tool(
            name="Azure",
            func=AzureDevopsChain(
                llm=self.llm,
                verbose=True,
                token=auth["token"],
                org=auth["org"],
            ).run,
            description="Useful when you need to manage or read information from Azure DevOps about projects or the company",
        )

    def _get_notion_tool(self, auth: dict):
        return Tool(
            name="Notion",
            func=NotionChain(
                llm=self.llm,
                verbose=True,
            ).run,
            description="Use only when user explicitly asks you to create a Notion page",
        )
