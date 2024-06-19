from logging import Logger
from typing import List

from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI

from equivalent_llm.engine import PromptEngine
from equivalent_llm.parse import json_loads

class OpenAI(PromptEngine):

    configurations = {
        'temperature': 0.15,
        'top_p': 1.0,
        'model': 'gpt-4o',
    }

    def __init__(self, logger: Logger, **kwargs):
        configurations = self.configurations.copy()
        configurations.update(kwargs)
        model = configurations.pop('model')
        temperature = configurations.pop('temperature')

        self.chat = ChatOpenAI(model=model, temperature=temperature, model_kwargs=configurations)
        self.logger = logger

    def invoke(self, messages: List[BaseMessage]) -> dict:
        response = self.chat.invoke(messages)
        self.logger.debug(f"### OpenAI response: {response}")

        result = response.content
        # markdown json format
        if isinstance(result, str):
            if result.startswith("```json"):
                return json_loads(result.split("```json")[1].split("```")[0])
            else:
                return json_loads(result)
        else:
            raise ValueError(f"Unexpected response type: {type(result)}")
