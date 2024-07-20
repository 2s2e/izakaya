from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

import dotenv
import os


dotenv.load_dotenv()
# Initialize the OpenAI tool with your API key
openai_model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


class ChineseConversationAgent:
    def __init__(self):
        self.context = []

    def execute(self, input_text, orig_prompt=None):

        openai_model.invoke([HumanMessage(content=input_text)])
