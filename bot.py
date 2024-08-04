from openai import OpenAI
from dotenv import load_dotenv
import os
import iza_utils
import time
from colorama import Fore, Back, Style
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class Bot:
    def __init__(self, prompt, model="gpt-4o", temperature=0.5):
        # self.prompt = prompt
        # self.history = [{"role": "system", "content": prompt}]
        self.model = "gpt-4o"

        load_dotenv()
        # self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.prompt = prompt
        self.llm = ChatOpenAI(temperature=temperature, model=model)
        self.history = [SystemMessage(content=self.prompt)]

    def speak(self):
        response = self.llm.invoke(self.history)
        self.history.append(AIMessage(content=response.content))

        return response.content

    # response = self.llm.invoke(self.history)
    #     self.history.append(
    #         {
    #             "role": "assistant",
    #             "content": response.choices[0].message.content.strip(),
    #         }
    #     )

    #     return response.choices[0].message.content

    def listen(self, user_input):
        # self.history.append({"role": "user", "content": user_input})
        self.history.append(HumanMessage(content=user_input))

    def get_history(self):
        return self.history

    def reset_history(self):
        self.history = [SystemMessage(content=self.prompt)]
        pass
