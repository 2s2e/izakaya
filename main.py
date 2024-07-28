from dialogue import ChineseConversationAgent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from colorama import Fore, Back, Style

# agent = ChineseConversationAgent()
from openai import OpenAI
from dotenv import load_dotenv
import os
import iza_utils
import time

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
MAX_CONVERSATION_LENGTH = 7

conversation_prompt = iza_utils.get_conversation_prompt()


# response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": orig_prompt}])
history = [{"role": "system", "content": conversation_prompt}]

while len(history) < MAX_CONVERSATION_LENGTH:
    # bot response
    response = client.chat.completions.create(model=MODEL, messages=history)
    print(Fore.LIGHTCYAN_EX + "Bot:", response.choices[0].message.content)
    print(Style.RESET_ALL)
    history.append(
        {"role": "assistant", "content": response.choices[0].message.content.strip()}
    )

    #

    # user response
    user_input = input(Fore.LIGHTWHITE_EX + "User: ")
    print(Style.RESET_ALL)
    history.append({"role": "user", "content": user_input})

history_for_review = iza_utils.convert_history_to_string(history)

correction_prompt = """
Please review the conversation below and correct any mistakes made by the user.
{history}

Give an overall evaluation of how the user did, and then please deep dive into each specific mistake made by the user.
You should give this evaluation as if you are talking to the user, because you are. 

Give the evaluation in ENGLISH please
""".format(
    history=history_for_review, language=languages[0]
)

response = client.chat.completions.create(
    model=MODEL, messages=[{"role": "user", "content": correction_prompt}]
)
print(Fore.LIGHTMAGENTA_EX + "Bot:", response.choices[0].message.content)
print(Style.RESET_ALL)

# save conversation
conversation = iza_utils.convert_history_to_string(history)
# save file as urrent timestamp
filename = "conversations/{}.txt".format(str(time.time))
conversation_file = open(filename, "w")
conversation_file.write(conversation)
