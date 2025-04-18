"""Chain that interprets a prompt and runs an Azure CLI command to answer it"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Extra
from ...utils.AzureDevops.commands import command_list
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.prompts.base import BasePromptTemplate
from .command_executor import CommandExecutor
from .prompt import PROMPT
from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
)


class AzureDevopsChain(Chain, BaseModel):
    llm: BaseLLM
    prompt: BasePromptTemplate = PROMPT
    org: str
    token: str

    input_key: str = "question"
    output_key: str = "answer"

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def _process_llm_result(
        self, text: str, run_manager: CallbackManagerForChainRun
    ) -> Dict[str, str]:
        az_executor = CommandExecutor()
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        _run_manager.on_text(text, color="blue", verbose=self.verbose)
        text = text.strip()
        output = ""
        if text.startswith("Command: "):
            command = text[9:]
            output = az_executor.execute(command, self.token, self.org).get_output()
            _run_manager.on_text("\nOutput: ", verbose=self.verbose)
            _run_manager.on_text(output, color="green", verbose=self.verbose)
            output = "Output: " + output
        else:
            raise ValueError("Invalid output from LLM: " + text)

        return {self.output_key: output}

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        llm_executor = LLMChain(
            prompt=self.prompt, llm=self.llm, callback_manager=self.callback_manager
        )
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        _run_manager.on_text(inputs[self.input_key], verbose=self.verbose)
        text = llm_executor.predict(
            question=inputs[self.input_key], commands=str(command_list), stop=["stop"]
        )
        return self._process_llm_result(text, run_manager=_run_manager)

    @property
    def _chain_type(self) -> str:
        return "azure_devops_chain"
