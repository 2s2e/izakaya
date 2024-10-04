from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage


def convert_history_to_string(history: list[BaseMessage]) -> str:
    message_string = ""
    for message in history:
        if isinstance(message, AIMessage):
            message_type = "AI"
        elif isinstance(message, HumanMessage):
            message_type = "Human"
        elif isinstance(message, SystemMessage):
            message_type = "System"
        else:
            message_type = "Unknown"

        message_string += f"{message_type}: {message.content}\n"
    return message_string.strip()


def get_target():
    print("Choose a target skill:")
    possible_targets = [
        "Vocabulary: work related conversation",
        "Grammar: comparison",
        "Grammar: past tense",
        "Pick my own target skill",
    ]

    for i, target in enumerate(possible_targets):
        print(f"{i + 1}. {target}")

    target_choice = (
        int(input("Enter the number of the target you want to choose: ")) - 1
    )

    if target_choice == 3:
        custom_target = input("Enter your own target skill: ")
        return custom_target

    return possible_targets[target_choice]


def get_conversation_prompt():
    possible_topics = [
        "Vocabulary: work related conversation",
        "Grammar: comparison",
        "Grammar: past tense",
        "Pick my own",
    ]

    print("Choose a topic:")
    for i, topic in enumerate(possible_topics):
        print(f"{i + 1}. {topic}")

    topic_choice = int(input("Enter the number of the topic you want to choose: ")) - 1

    languages = ["Japanese", "Chinese", "Korean"]

    conversation_prompt = """
    You are a {language} conversation agent, who will teach the language  in the following situation:

    You are a bartender an izakaya. The human you are talking to is a new customer. Welcome him in and make conversation with him.
    As the bartender, you should be polite and professional. You should also be able to make small talk and engage in conversation with the customer.

    You should make conversation in a way that drills the user on the following areas of the {language} language:
    {topic}

    If the user makes any significant mistakes, make sure to STAY IN CHARACTER, and ask for only ask for clarification if the mistake obstructs the conversation.

    ONLY use {language} in your responses. Try to keep each of your phrases short, have a max of one inquiry per phrase.
    """.format(
        language=languages[0], topic=possible_topics[topic_choice]
    )

    return conversation_prompt


def save_session(conversation_string, feedback_string, prompt_string):
    filename = "../conversations/{}.txt".format(
        datetime.now().strftime("transcript %Y-%m-%d_%H-%M-%S")
    )

    filename2 = "../conversations/{}.txt".format(
        datetime.now().strftime("feedback %Y-%m-%d_%H-%M-%S")
    )

    filename3 = "../conversations/{}.txt".format(
        datetime.now().strftime("prompt %Y-%m-%d_%H-%M-%S")
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(conversation_string)

    with open(filename2, "w", encoding="utf-8") as file:
        file.write(feedback_string)

    with open(filename3, "w", encoding="utf-8") as file:
        file.write(prompt_string)
