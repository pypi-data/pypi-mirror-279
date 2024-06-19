import json
import logging
import os
import re
import requests
from logging import Logger
from typing import List, Union

from langchain_core.messages import AIMessage, BaseMessage, FunctionMessage, SystemMessage

from pydantic import BaseModel, Field

from equivalent_llm.engine import PromptEngine
from equivalent_llm.parse import json_loads

class PETUsage(BaseModel):
    promptTokens: int
    completionTokens: int
    totalTokens: int

class PETCompletionResponse(BaseModel):
    model: str
    transactionId: str
    content: str = Field(default=None)
    usage: PETUsage = Field(default=None)

class PETResponse(BaseModel):
    state: int
    res: PETCompletionResponse

class PET(PromptEngine):
    _DEFUALT_PET_URL = 'http://172.18.243.211:13100'
    _DEFAULT_PET_ID = '124102'
    _DEFAULT_PET_TIMEOUT = 60
    _DEFAULT_RETRYT = 3

    def __init__(self, logger: Logger, **kwargs):
        self.pet_id = os.environ['PET_ID'] if 'PET_ID' in os.environ else self._DEFAULT_PET_ID
        self.pet_url = os.environ['PET_URL'] if 'PET_URL' in os.environ else self._DEFUALT_PET_URL
        self.pet_timeout = int(os.environ['PET_TIMEOUT']) if 'PET_TIMEOUT' in os.environ else self._DEFAULT_PET_TIMEOUT
        self.retry = int(os.environ['PET_RETRY']) if 'PET_RETRY' in os.environ else self._DEFAULT_PET_TIMEOUT

        self.logger = logger

    def a(self) -> dict:
        return {}

    def _message_to_content(self, message: BaseMessage) -> dict:
        match message:
            case SystemMessage():
                return {"role": "system", "content": message.content}
            case AIMessage():
                return {"role": "ai", "content": message.content}
            case FunctionMessage():
                return {"role": "function", "content": message.content}
            case _:
                return {"role": "user", "content": message.content}

    def messages_to_contents(self, message: Union[BaseMessage, List[BaseMessage]]) -> str:
        if isinstance(message, list):
            return json.dumps([self._message_to_content(m) for m in message])
        else:
            return json.dumps([self._message_to_content(message)])

    def invoke(self, messages: List[BaseMessage]) -> dict:
        completion_url = f'{self.pet_url}/api/v1/completions'
        headers = {'Content-Type': 'application/json'}
        request_body = {
            'promptId': self.pet_id,
            'transactionId': 'movie-validation',
            'role': 'user',
            'requestTexts': [{'key': 'content', 'value': self.messages_to_contents(messages)}],
        }

        response = requests.post(url=completion_url, headers=headers, data=json.dumps(request_body), timeout=self.pet_timeout)
        count = self.retry - 1
        while (response.status_code // 100) != 2 and count > 0:
            response = requests.post(url=completion_url, headers=headers, data=json.dumps(request_body), timeout=self.pet_timeout)
            count -= 1
        if count <= 0:
            logging.error(f"### PET request failed: {response.status_code}: {request_body}")
        parsed_response = PETResponse(**json_loads(response.content))
        self.logger.debug(f"### PET response: {parsed_response}")

        result = parsed_response.res.content
        if not result.startswith("[") and not result.startswith("{"):
            found = re.search(r"```json.+```", result, flags=re.DOTALL)
            result = found.group() if found is not None else result
        if result.startswith("```json"):
            return json_loads(result.split("```json")[1].split("```")[0])
        else:
            return json_loads(result)
