from bot import Bot


def generate_character(context):
    prompt = """
        You are an expert author, experienced in building rich and detailed characters for stories. You have been tasked with creating a character 
        in a scenario, to really bring them to life. 

        Based on the scenario that you are given, craft me a detailed character that would fit the role of the AI Instructor.

        Note, the character DOES NOT HAVE ANYTHING TO DO WITH AI, THEY ARE JUST A CHARACTER IN A SCENARIO.

        Give me your character in the following format:

        Name:
        Age:
        Gender:
        Brief biography:

        Do not give me anything else.

        Here is the scenario you will be working with:
        {}
    """.format(
        context
    )

    bot = Bot(prompt=prompt, temperature=0.7)
    response = bot.speak()
    return response


def generate_context(target):
    prompt = """
        You are an expert language teacher, experienced in crafting perfect scenarios for students to practice their Japanese conversational skills.
        The scenarios you generate are detailed, and are perfectly tailored to what the student wants to improve. 

        Please generate a scenario, involving two people, the AI instructor and the user, that will force the student to practice the following target skill:
        {}

        Just generate the context, what is happening, the role of the user, and the role of the AI. Keep in mind that the personality and traits of the AI agent will
        be created by another bot, so don't worry about that. In the user role and AI insturctor role, DO NOT mention to target skill, nor that the user is trying to learn Japanese.

        If you can, try to mix up the relationship between the AI Instructor and the user a bit, the AI Instructor need not always be the friend of the user, though it certainly could be.

        AVOID formal business settings, and try to build the scenario in a way that encourages both sides to have short, snappy responses.

        Give me your response in the following format:

            Context: ...
            User's role: ...
            AI Instructor's role: ...

        Do not give me anything else.
    """.format(
        target
    )

    bot = Bot(prompt=prompt, temperature=0.7)
    response = bot.speak()
    return response


def generate_packaged_prompt(target, level="N4"):
    context = generate_context(target)
    character = generate_character(context)

    # print(context)
    # print(character)

    prompt = """
        You are a conversation agent, who will teach the language in the following situation:

        You will be playing the role of the following character:
        {}

        You will be engaging in a conversation with the student, in the following scenario:
        {}

        You should make conversation in a way that drills the user on the following areas of the Japanese language:
        {}

        If the user makes any significant mistakes, make sure to STAY IN CHARACTER, and ask for only ask for clarification if the mistake obstructs the conversation.

        ONLY use Japanese in your responses. 
        It is IMPERATIVE that you stay in character, and do not break character at any point.

        The user is currently of Japanese level {}, so keep this in mind when considering the complexity of your responses.

        Now, make an extremely BRIEF introduction, and then follow along with the conversation, keeping your responses SHORT

    """.format(
        character, context, target, level
    )
    bot = Bot(prompt=prompt)
    response = bot.speak()
    prompt2 = """
        Next, generate a paragraph summary of the role between user and AI Instructor in the scenario you just created, as well as the character you created.
        This will be given to the user. 
        Please give this summary in ENGLISH.
    """
    bot.listen(prompt2)
    response2 = bot.speak()
    return prompt, response2


if __name__ == "__main__":
    target = "Vocabulary: work related conversation"
    context = generate_context(target)
    # print(context)
    # print(generate_character(context))
