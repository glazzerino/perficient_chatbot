import os
from langchain.agents import Tool
from langchain.llms import OpenAI
from chains.azure.base import AzureDevopsChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import load_tools
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)

llm = OpenAI(temperature=0.0)

# Load credentials from environment variables
token = os.environ.get("AZURE_DEVOPS_TOKEN")
org = os.environ.get("AZURE_DEVOPS_ORG")

if not token or not org:
    raise ValueError("AZURE_DEVOPS_TOKEN and AZURE_DEVOPS_ORG environment variables must be set")

azure_chain = AzureDevopsChain(
    llm=llm,
    verbose=True,
    token=token,
    org=org,
)

tools = [
    Tool(
        name="Azure",
        func=azure_chain.run,
        description="Useful when you need to manage or read information from Azure DevOps about projects or the company",
    ),
]


def initialize_environment():
    with open(".env", "r") as f:
        for line in f:
            key, value = line.split("=")
            os.environ[key] = value


def run_chatbot(input_text):
    memory = ConversationBufferMemory()
    planner = load_chat_planner(llm)
    executor = load_agent_executor(llm, tools, verbose=True)
    agent = PlanAndExecute(
        planner=planner, executer=executor, memory=memory, verbose=True
    )

    output = agent.run(input=input_text)
    return output


def main():
    input_text = input("Enter your message: ")
    output = run_chatbot(input_text)
    print(output)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            continue
