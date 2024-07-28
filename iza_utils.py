from datetime import datetime


def convert_history_to_string(history):
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])


def get_conversation_prompt():
    possible_topics = [
        "Vocabulary: work related conversation",
        "Grammar: comparison",
        "Grammar: past tense",
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


def save_session(conversation_string, feedback_string):
    filename = "conversations/{}.txt".format(
        datetime.now().strftime("transcript %Y-%m-%d_%H-%M-%S")
    )

    filename2 = "conversations/{}.txt".format(
        datetime.now().strftime("feedback %Y-%m-%d_%H-%M-%S")
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(conversation_string)

    with open(filename2, "w", encoding="utf-8") as file:
        file.write(feedback_string)
