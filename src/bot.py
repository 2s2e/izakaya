from openai import OpenAI
from dotenv import load_dotenv
import os
import iza_utils
import time
from colorama import Fore, Back, Style
from langchain_openai import ChatOpenAI
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
from langdetect import detect
from colorama import Fore, Back, Style


class Bot:
    def __init__(self, prompt, model="gpt-4o", temperature=0.5):

        # define the model
        self.model = "gpt-4o"

        # load environment variables
        load_dotenv()

        self.prompt = prompt
        self.llm = ChatOpenAI(temperature=temperature, model=model)
        self.history = [SystemMessage(content=self.prompt)]

    # generate a response to speak based on message history, and append to history
    def speak(self):
        response = self.llm.invoke(self.history)
        self.history.append(AIMessage(content=response.content))

        return response.content

    # listen to user_input, and put in history
    def listen(self, user_input):
        # self.history.append({"role": "user", "content": user_input})
        self.history.append(HumanMessage(content=user_input))

    # return history
    def get_history(self):
        return self.history

    # reset history
    def reset_history(self):
        self.history = [SystemMessage(content=self.prompt)]
        pass


class ReviewBot(Bot):
    def __init__(self, prompt, model="gpt-4o", temperature=0.5):

        self.model = "gpt-4o"
        load_dotenv()

        self.prompt = prompt
        self.llm = ChatOpenAI(temperature=temperature, model=model)
        self.history = [SystemMessage(content=self.prompt)]

        # prompt for assisting the user mid conversation
        self.help_prompt = """
        You are a Japanese coach, and a student has just asked you for assistance with a conversation they are having with the practice partner.

        The student has just asked you a question, and you respond in a way that will help them with their Japanese skills. 

        Respond as if you are teaching someone who's mother tongue is English please, and you are teaching them Japanese.

        Start you sentence an encouraging remark in English. 
        """
        self.help_history = []
        self.help_history.append(SystemMessage(content=self.help_prompt))

        # prompt for giving user feedback
        self.review_prompt = """
            You are helping a student review a conversation. The scenario was as follows: {prompt}.

            You will be given parts of a conversation to review, and you will be asked to give feedback on the student's performance.

            Please be specific in your feedback, taking into account grammar, vocabulary use, and conversational correctness. Be thorough. 
        """

        # history for review
        self.review_history = []
        self.review_history.append(SystemMessage(content=self.review_prompt))

    def speak(self):
        prev_message = self.help_history[-1]
        # if the user response was not in japanese, provide assistance
        if (
            detect(prev_message.content) != "ja"
            and type(prev_message) == HumanMessage
            and ("HUM" not in prev_message.content[0:3])
        ):
            response = self.llm.invoke(self.help_history)
            return response.content
        # otherwise, review
        else:
            response = self.llm.invoke(self.review_history)
            return response.content

    def listen(self, user_input):
        self.review_history.append(HumanMessage(content=user_input))

    def get_history(self):
        return self.history

    def reset_history(self):
        self.history = [SystemMessage(content=self.prompt)]
        pass


class TutorBot(Bot):
    def __init__(self, prompt, model="gpt-4o", temperature=0.5):
        super().__init__(prompt, model, temperature)
        self.help_prompt = """
        You are a Japanese coach, and a student has just asked you for assistance with a conversation they are having with the practice partner.

        The student has just asked you a question, and you respond in a way that will help them with their Japanese skills. 

        Respond as if you are teaching someone who's mother tongue is English please, and you are teaching them Japanese.

        Start you sentence an encouraging remark in English. 
        """
        self.help_history = []
        self.help_history.append(SystemMessage(content=self.help_prompt))

    def speak(self):
        prev_message = self.help_history[-1]

        if detect(prev_message.content) != "ja" and type(prev_message) == HumanMessage:
            response = self.llm.invoke(self.help_history)
            self.help_history.append(AIMessage(content=response.content))
            return response.content
        else:
            response = self.llm.invoke(self.history)
            self.help_history.append(AIMessage(content=response.content))
            self.history.append(AIMessage(content=response.content))
            return response.content

    def listen(self, user_input):
        self.help_history.append(HumanMessage(content=user_input))
        if detect(user_input) != "en":
            self.history.append(HumanMessage(content=user_input))

    def get_history(self):
        return self.history

    def get_full_history(self):
        return self.help_history

    def reset_history(self):
        self.history = [SystemMessage(content=self.prompt)]
        self.help_history = [SystemMessage(content=self.help_prompt)]
        self.memory.clear()
