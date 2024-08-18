from datetime import datetime
from pathlib import Path
import threading
import wave
import sounddevice as sd
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
from bot import Bot, TutorBot

from scenario import generate_context, generate_character, generate_packaged_prompt

recording_stop = False


def record_audio(filename="output.wav", fs=44100):
    global recording_stop
    print("Please speak... Press Enter to stop recording.")

    # Start a thread to monitor for a keypress
    threading.Thread(target=stop_recording_on_keypress).start()

    recording = []  # List to hold chunks of audio data

    while not recording_stop:
        # Record in small chunks
        chunk = sd.rec(int(fs * 0.1), samplerate=fs, channels=1, dtype="int16")
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
    openai.api_key = os.getenv("OPENAI_API_KEY")
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]


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


def speech_loop(conv_bot, max_length):
    client = OpenAI()
    p = pyaudio.PyAudio()
    while len(conv_bot.get_history()) < max_length:
        # bot response

        # get the response from the bot
        text_response = conv_bot.speak()
        print(Fore.LIGHTCYAN_EX + "Bot:", text_response, Style.RESET_ALL)
        # get the audio stream
        response = client.audio.speech.create(
            model="tts-1", voice="alloy", input=text_response
        )
        # output audio stream
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,  # This rate should match the TTS output rate
            output=True,
        )
        # Stream the audio data directly to the playback stream
        for (
            chunk
        ) in (
            response.iter_bytes()
        ):  # Assume the response supports a `.stream()` generator
            stream.write(chunk)
        stream.stop_stream()
        stream.close()

        ### user response
        record_audio()
        user_input = transcribe_audio("output.wav")
        print(Fore.LIGHTWHITE_EX, user_input, Style.RESET_ALL)
        conv_bot.listen(user_input)

    p.terminate()


load_dotenv()
