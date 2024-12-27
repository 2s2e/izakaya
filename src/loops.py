from datetime import datetime
import io
from pathlib import Path
import threading
import wave
from langdetect import detect
import sounddevice as sd
import soundfile as sf
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from colorama import Fore, Back, Style

# agent = ChineseConversationAgent()
from openai import OpenAI
from dotenv import load_dotenv
import os

import openai
import iza_utils
import time
import pyaudio
import numpy as np
from bot import Bot, TutorBot, ReviewBot

from scenario import generate_context, generate_character, generate_packaged_prompt

recording_stop = False


def record_audio(filename="output.wav", fs=44100):
    global recording_stop
    recording_stop = False
    print("Please speak... Press Enter to stop recording.")

    # Start a thread to monitor for a keypress
    threading.Thread(target=stop_recording_on_keypress).start()

    recording = []  # List to hold chunks of audio data

    while not recording_stop:
        # Record in small chunks
        chunk = sd.rec(int(fs * 5), samplerate=fs, channels=1, dtype="int16")
        sd.wait()  # Wait until the chunk is finished
        recording.append(chunk)

    # Concatenate all chunks
    recording = np.concatenate(recording, axis=0)
    print("Recording finished.")

    # Save as WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())


def stop_recording_on_keypress():
    global recording_stop
    input()  # Wait for the Enter key press
    recording_stop = True


# Function to transcribe audio using Whisper API
def transcribe_audio(file_path):
    client = OpenAI()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    transcript = None
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, language="ja"
        )
    return transcript.text


# loop for doing a typed conversation
def type_loop(conv_bot, max_length):
    while len(conv_bot.get_history()) < max_length:
        # bot response
        response = conv_bot.speak()
        print(Fore.LIGHTCYAN_EX + "Bot:", response)
        print(Style.RESET_ALL)

        # user response
        user_input = input(Fore.LIGHTWHITE_EX + "User: ")
        print(Style.RESET_ALL)
        conv_bot.listen(user_input)


# loop for doing a spoken conversation
def speech_loop(conv_bot, max_length):
    client = OpenAI()
    p = pyaudio.PyAudio()
    while len(conv_bot.get_history()) < max_length:
        # bot response

        # get the response from the bot
        text_response = conv_bot.speak()
        response = client.audio.speech.create(
            model="tts-1", voice="alloy", input=text_response
        )
        print(Fore.LIGHTCYAN_EX + "Bot:", text_response, Style.RESET_ALL)

        buffer = io.BytesIO()
        for chunk in response.iter_bytes(chunk_size=4096):
            buffer.write(chunk)
        buffer.seek(0)

        with sf.SoundFile(buffer, "r") as sound_file:
            data = sound_file.read(dtype="int16")
            sd.play(data, sound_file.samplerate)
            sd.wait()

        ### user response
        record_audio()
        user_input = transcribe_audio("output.wav")
        print(Fore.LIGHTWHITE_EX, user_input, Style.RESET_ALL)
        conv_bot.listen(user_input)

    p.terminate()


# loop for putting it all together
def main_loop(is_audio=False):
    # get the targeted skill, the prompt for the conversation
    target = iza_utils.get_target()
    conversation_prompt, summary = generate_packaged_prompt(target, level="beginner")

    # setup
    print(Fore.LIGHTYELLOW_EX + summary + Style.RESET_ALL)
    conv_bot = TutorBot(prompt=conversation_prompt, temperature=0.3)

    # get the conversation length from environment
    MAX_CONVERSATION_LENGTH = int(os.getenv("MAX_CONVERSATION_LENGTH"))

    while len(conv_bot.get_history()) < MAX_CONVERSATION_LENGTH:

        if is_audio:
            speech_loop(conv_bot, MAX_CONVERSATION_LENGTH)
        else:
            type_loop(conv_bot, MAX_CONVERSATION_LENGTH)

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

    iza_utils.save_session(shortened, feedback, conversation_prompt)


def review_loop():
    conversation, _, prompt = iza_utils.get_session_to_review()
    review_bot = ReviewBot(prompt=prompt)

    i = 0
    while i < len(conversation):
        # color to cyan for bot response
        print(Fore.LIGHTCYAN_EX + "Your conversation partner said:", conversation[i][1])
        # color to white for your response as the user
        print(Fore.LIGHTWHITE_EX + "You said:", conversation[i + 1][1])
        # color to magenta for the feedback
        review_bot.listen(
            """HUM: Given the following exchange between the bot and the AI, can you correct any mistakes the user made 
                          as well as give them suggestions for how to improve their response and tell them to try again?
                          Bot: {} User: {}""".format(
                conversation[i][1], conversation[i + 1][1]
            )
        )
        feedback = review_bot.speak()
        print(Fore.LIGHTMAGENTA_EX + "Feedback:", feedback)

        user_input = ""

        while user_input == "" or detect(user_input) != "ja":
            user_input = input(Fore.LIGHTWHITE_EX + "")
            print(Style.RESET_ALL)
            review_bot.listen(user_input)
            feedback = review_bot.speak()
            print(Fore.LIGHTMAGENTA_EX + "Feedback:", feedback)

        print(Fore.CYAN)
        try_again = input("Would you like to try again? (y/n): ")
        if try_again == "y":
            conversation[i + 1][1] = user_input
        else:
            i += 2


load_dotenv()
