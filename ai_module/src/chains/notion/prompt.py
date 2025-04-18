from langchain.prompts.prompt import PromptTemplate

_PROMPT_TEMPLATE = """
You are an intelligent assistant tasked with creating notes on a service
called Notion.

Based on the user's input and instruction, you will generate 
a title and a paragraph for the new note in question.

Start
Input: {{raw data that you will work with}}

Title: {{title you will come up with based on the input data}}
Paragraph: {{paragraph you will come up with}}
Stop

Start
Input: {input}

"""

PROMPT = PromptTemplate(input_variables=["input"], template=_PROMPT_TEMPLATE)
