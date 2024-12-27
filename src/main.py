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
from loops import type_loop, speech_loop, main_loop, review_loop

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

# new options menu

print(
    "Please select an option: \n 1. Start text conversation \n 2. Start voice conversation \n 3. Review a previous session"
)
demo_choice = input("Choose an option: \n")


# is_demoing = False
# if demo_choice == "1":
#     is_demoing = True

# driver
if demo_choice == "1":
    main_loop()
elif demo_choice == "2":
    main_loop(True)
elif demo_choice == "3":
    review_loop()
