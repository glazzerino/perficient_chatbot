"""Chain that creates a new page in Notion with the given information"""
from typing import Dict, List, Optional
from .prompt import PROMPT
from langchain.prompts.base import BasePromptTemplate
from pydantic import BaseModel, Extra
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
)
import sys

sys.path.append("src")
from ai_module.src.chains.notion.notion_wrapper import NotionWrapper
import re


class NotionChain(Chain, BaseModel):
    llm: BaseLLM
    prompt: BasePromptTemplate = PROMPT
    notion: NotionWrapper = NotionWrapper()

    input_key: str = "input"
    output_key: str = "response"

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

    def _extract_generated_text(self, generated_text):
        try:
            title = re.search(r"Title: (.+?)\n", generated_text).group(1)
            paragraph = re.search(
                r"Paragraph: (.+)\n?", generated_text, re.DOTALL
            ).group(1)
            return title, paragraph
        except AttributeError:
            # Handle the case where the regex pattern doesn't match
            raise ValueError(
                "Failed to extract title and paragraph from generated text."
            )

    def _process_llm_result(
        self, text: str, run_manager: CallbackManagerForChainRun
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        _run_manager.on_text(text, color="blue", verbose=self.verbose)

        text = text.strip()
        output = ""
        try:
            title, paragraph = self._extract_generated_text(text)
            response = self.notion.create_page(title, paragraph)
            output = response.text
        except ValueError as error:
            _run_manager.on_text(str(error), color="red", verbose=self.verbose)
            output = str(error)

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
        text = llm_executor.predict(input=inputs[self.input_key], stop=["stop"])
        return self._process_llm_result(text, run_manager=_run_manager)

    @property
    def _chain_type(self) -> str:
        return "notion_chain"
