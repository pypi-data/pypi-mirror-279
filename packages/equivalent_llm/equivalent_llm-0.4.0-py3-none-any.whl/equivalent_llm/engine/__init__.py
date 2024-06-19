from typing import List

from langchain_core.messages.base import BaseMessage

class PromptEngine:
    def invoke(self, messages: List[BaseMessage]) -> dict:
        raise NotImplementedError()
