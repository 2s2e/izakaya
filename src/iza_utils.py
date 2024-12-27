from datetime import datetime
import os
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
import json


# method for converting a list of messages to a string
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


# convert a list of messages to a list of strings
def convert_history_to_list(history: str) -> list[BaseMessage]:
    toRet = []
    for message in history:
        if isinstance(message, AIMessage):
            message_type = "AI"
        elif isinstance(message, HumanMessage):
            message_type = "Human"
        elif isinstance(message, SystemMessage):
            message_type = "System"
        else:
            message_type = "Unknown"

        toRet.append([message_type, message.content])
    return toRet


# prompt for the target skill
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


# prompt the user for the session to review
def get_session_to_review():
    session_files = os.listdir("../conversations")
    files = []
    for i, session_file in enumerate(session_files):
        # only show json files
        if session_file.endswith(".json"):
            files.append(session_file)

    for i, session_file in enumerate(files):
        print(f"{i + 1}. {session_file}")

    session_choice = (
        int(input("Enter the number of the session you want to review: ")) - 1
    )

    with open(f"../conversations/{files[session_choice]}", "r") as file:
        data = json.load(file)
        print(data)
        conversation = data["conversation"]
        feedback = data["feedback"]
        prompt = data["prompt"]

    return conversation, feedback, prompt


# write everything to a single json file
def save_session(conversation, feedback_string, prompt_string):
    filename = "../conversations/{}.json".format(
        datetime.now().strftime("session %Y-%m-%d_%H-%M-%S")
    )

    print(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    data = {}
    conversation_list = convert_history_to_list(conversation)
    data["conversation"] = conversation_list
    data["prompt"] = prompt_string
    data["feedback"] = feedback_string

    json_data = json.dumps(data, indent=4)

    # write json_data to file
    with open(filename, "w") as file:
        file.write(json_data)
