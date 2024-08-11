from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from colorama import Fore, Back, Style

# agent = ChineseConversationAgent()
from openai import OpenAI
from dotenv import load_dotenv
import os
import iza_utils
import time
from bot import Bot, TutorBot

from scenario import generate_context, generate_character, generate_packaged_prompt

# while True:
#     orig_prompt = """
#     You are a Chinese conversation agent in the following situation:

#     You are a bartender at an upscale lounge. The human you are talking to is a new customer. Welcome him in and make conversation with him.
#     As the bartender, you should be polite and professional. You should also be able to make small talk and engage in conversation with the customer.

#     You should make conversation in a way that drills the user on the following areas of the Chinese language:
#     measure words
#     comparison
#     """
#     user_input = input("User: ")
#     actions = agent.plan(user_input, orig_prompt=orig_prompt)
#     results = agent.execute(actions)
#     print("Bot:", results["respond"])

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print(Style.RESET_ALL)

MODEL = "gpt-4o"
MAX_CONVERSATION_LENGTH = 3

target = iza_utils.get_target()
conversation_prompt, summary = generate_packaged_prompt(target, level="beginner")

print(Fore.LIGHTYELLOW_EX + summary + Style.RESET_ALL)

conv_bot = TutorBot(prompt=conversation_prompt, temperature=0.3)
while len(conv_bot.get_history()) < MAX_CONVERSATION_LENGTH:
    # bot response
    response = conv_bot.speak()
    print(Fore.LIGHTCYAN_EX + "Bot:", response)
    print(Style.RESET_ALL)

    # user response
    user_input = input(Fore.LIGHTWHITE_EX + "User: ")
    print(Style.RESET_ALL)
    conv_bot.listen(user_input)

history_for_review = iza_utils.convert_history_to_string(conv_bot.get_history())


correction_prompt = """
Please review the conversation below and correct any mistakes made by the user.
{history}

Give an overall evaluation of how the user did, and then please deep dive into each specific mistake made by the user.
You should give this evaluation as if you are talking to the user, because you are. 

Give the evaluation in ENGLISH please
""".format(
    history=history_for_review, language="Japanese"
)

correction_bot = Bot(prompt=correction_prompt)

response = correction_bot.speak()
print(Fore.LIGHTMAGENTA_EX + "Bot:", response)
print(Style.RESET_ALL)

feedback = response
shortened = conv_bot.get_history()[1:]
conversation = iza_utils.convert_history_to_string(shortened)

iza_utils.save_session(conversation, feedback, conversation_prompt)
