import os
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from chains.azure.base import AzureDevopsChain
import streamlit as st
from streamlit_chat import message
from langchain.memory import ConversationBufferMemory
from langchain.agents import load_tools
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from chains.notion.base import NotionChain


def load_env():
    with open(".env", "r") as f:
        for line in f:
            key, value = line.split("=")
            os.environ[key] = value


llm = OpenAI(temperature=0.0, model_name="text-davinci-003")

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
notion_chain = NotionChain(llm=llm, verbose=True)
tools = [
    Tool(
        name="Azure",
        func=azure_chain.run,
        description="Useful when you need to manage or read information from Azure DevOps about projects or the company",
    ),
    Tool(
        name="Notion",
        func=notion_chain.run,
        description="Useful when the user asks to create a new notion page.",
    ),
]


if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory()

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, verbose=True)
agent = PlanAndExecute(
    planner=planner,
    executer=executor,
    memory=st.session_state["memory"],
    verbose=True,
)

st.title("Azure DevOps Chatbot Demo")


def get_input():
    input_text = st.text_input("watchu want?")
    return input_text


user_input = get_input()

if user_input:
    output = agent.run(input=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:
    print(st.session_state["memory"])
    for i in range(len(st.session_state["generated"])):
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
        message(st.session_state["generated"][i], key=str(i))
