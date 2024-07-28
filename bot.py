from openai import OpenAI
from dotenv import load_dotenv
import os
import iza_utils
import time
from colorama import Fore, Back, Style


class Bot:
    def __init__(self, prompt, model="gpt-4o"):
        self.prompt = prompt
        self.history = [{"role": "system", "content": prompt}]
        self.model = "gpt-4o"

        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        pass

    def speak(self):
        response = self.client.chat.completions.create(
            model=self.model, messages=self.history
        )
        self.history.append(
            {
                "role": "assistant",
                "content": response.choices[0].message.content.strip(),
            }
        )

        return response.choices[0].message.content

    def listen(self, user_input):
        self.history.append({"role": "user", "content": user_input})

    def reset_history(self):
        self.history = [{"role": "system", "content": self.prompt}]
        pass
