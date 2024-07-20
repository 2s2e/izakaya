from dialogue import ChineseConversationAgent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# agent = ChineseConversationAgent()
from openai import OpenAI
from dotenv import load_dotenv
import os

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

possible_topics = ["the difference between は and が", "measure words", "conditionals"]

MODEL = "gpt-4o"
orig_prompt = """
You are a Japanese conversation agent in the following situation:

You are a bartender at an upscale lounge. The human you are talking to is a new customer. Welcome him in and make conversation with him.
As the bartender, you should be polite and professional. You should also be able to make small talk and engage in conversation with the customer.

You should make conversation in a way that drills the user on the following areas of the Japanese language:
{}
""".format(
    possible_topics[0]
)
# response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": orig_prompt}])
history = [{"role": "system", "content": orig_prompt}]

while True:
    # bot response
    response = client.chat.completions.create(model=MODEL, messages=history)
    print("Bot:", response.choices[0].message.content)
    history.append(
        {"role": "assistant", "content": response.choices[0].message.content.strip()}
    )

    # user response
    user_input = input("User: ")
    history.append({"role": "user", "content": user_input})
