from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent

from dataclasses import dataclass
from typing import List, Optional, Union

from langchain.schema import BaseMessage, SystemMessage
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts.chat import (
    BaseMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from agent_openai_functions_custom.prompt import PROMPT


class CustomOpenAIFunctionsAgent(OpenAIFunctionsAgent):
    @classmethod
    def create_prompt(
        cls, custom_system_message: Optional[str] = None
    ) -> BasePromptTemplate:
        # Use the custom system message if provided, otherwise default to the parent class message
        if custom_system_message is not None:
            system_message = SystemMessage(content=custom_system_message)
        else:
            system_message = SystemMessage(content=PROMPT)

        # The rest of the method is copied from the parent class
        messages: List[Union[BaseMessagePromptTemplate, BaseMessage]]
        if system_message:
            messages = [system_message]
        else:
            messages = []

        messages.extend(
            [
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        input_variables = ["input", "agent_scratchpad"]
        return ChatPromptTemplate(input_variables=input_variables, messages=messages)
