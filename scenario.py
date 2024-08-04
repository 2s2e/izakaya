from bot import Bot


def generate_character(context):
    prompt = """
        You are an expert author, experienced in building rich and detailed characters for stories. You have been tasked with creating a character 
        in a scenario, to really bring them to life. 

        Based on the scenario that you are given, craft me a detailed character that would fit the role of the AI instructor.

        Give me your character in the following format:

        Name:
        Age:
        Gender:
        Occupation:
        3 Character Traits:
        3 Facts about their past:
        Brief biography:

        Do not give me anything else.

        Here is the scenario you will be working with:
        {}
    """.format(
        context
    )

    bot = Bot(prompt=prompt, temperature=0.9)
    response = bot.speak()
    return response


def generate_context(target):
    prompt = """
        You are an expert language teacher, experienced in crafting perfect scenarios for students to practice their Japanese conversational skills.
        The scenarios you generate are detailed, and are perfectly tailored to what the student wants to improve. 

        Please generate a scenario, involving two people, the AI instructor and the user, that will force the student to practice the following target skill:
        {}

        Just generate the context, what is happening, the role of the user, and the role of the AI. Keep in mind that the personality and traits of the AI agent will
        be created by another bot, so don't worry about that.

        If you can, try to mix up the relationship between the AI Instructor and the user a bit, the AI Instructor need not always be the friend of the user, though it certainly could be.

        Give me your response in the following format:

            Context: ...
            User's role: ...
            AI Instructor's role: ...

        Do not give me anything else.
    """.format(
        target
    )

    bot = Bot(prompt=prompt, temperature=0.9)
    response = bot.speak()
    return response


def generate_packaged_prompt(target):
    context = generate_context(target)
    character = generate_character(context)

    print(context)
    print(character)

    prompt = """
        You are an expert Japanese conversationalist, experienced with all the nuances and intricacies of Japanese. 

        You will be playing the role of the following character:
        {}

        You will be engaging in a conversation with the student, in the following scenario:
        {}

        You should make conversation in a way that drills the user on the following areas of the Japanese language:
        {}

        If the user makes any significant mistakes, make sure to STAY IN CHARACTER, and ask for only ask for clarification if the mistake obstructs the conversation.

        ONLY use Japanese in your responses. Try to keep each of your phrases short, have a max of one inquiry per phrase.
    """.format(
        character, context, target
    )
    bot = Bot(prompt=prompt)
    response = bot.speak()
    return response


if __name__ == "__main__":
    target = "Vocabulary: work related conversation"
    context = generate_context(target)
    print(context)
    print(generate_character(context))
