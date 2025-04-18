from abc import ABC, abstractmethod


class AssistantWrapperInterface(ABC):
    @abstractmethod
    def run_prompt(self, prompt: str, context: dict, auth: dict) -> str:
        pass
