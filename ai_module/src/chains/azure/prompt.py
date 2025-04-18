from langchain.prompts.prompt import PromptTemplate

_PROMPT_TEMPLATE = """
You are GPT, and you need to perform an action related to Azure DevOps.
You have access to a CLI tool that enables you to interact with Azure DevOps.

You can use the following commands: {commands}
Do not use anything other than the commands listed above.

Question: ${{Question or prompt to be answered or executed on Azure DevOps}}
Command: ${{Command that you will write}}

Begin:
Question: list of ppl?
Command: get_employees --query value[].{{name:displayName, email: mailAddress, avatar: _links.avatar.href}}
stop
Question: is there a David in the company?
Command: get_employees --query value[?contains(displayName, 'David')].{{name:displayName, email: mailAddress, avatar: _links.avatar.href}}
stop
Question: list my azure projects plz
Command: get_projects --project Chikapú --query value[].{{name:name, description:description}}
stop
Question: show work item 20 from Chikapú
Command: get_work_item --project Chikapú --ids 20
stop
Question: show work items 20, 21, 22 from Chikapú
Command: get_work_items --project Chikapú --ids 20 21 22
stop
Question: new task for Chikapú for bug fixing, type Task
Command: create_work_item --project Chikapú  --type Task --title "Bug fixing"
stop
Question: list ppl in my devops plz
Command: get_employees
stop
Question: new workitem for Chikapú about new feature, type Epic, assign to Francisco
Command: create_work_item --project Chikapú --type Epic --title "New feature" --assigned "a01570484@tec.mx"
stop
Question: update work item 20 from Chikapú, title: "New title", description: "New description", assigned to Francisco"
Command: update_work_item --project Chikapú --ids 20 --title "New title" --description "New description" --assigned a01570484@tec.mx"
stop
Question: update workitem 165 from project Chikapú, assign Francisco to it. His email is a01570484@tec.mx
Command: update_work_item --project Chikapú --ids 165 --assigned a01570484@tec.mx
stop
Question: {question}
"""

PROMPT = PromptTemplate(
    input_variables=["question", "commands"], template=_PROMPT_TEMPLATE
)
