import speech_recognition as sr
import pyttsx3
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = openai.OpenAI(api_key=OPENAI_KEY)


def speak_text(command):
    """Convert text to speech"""
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


r = sr.Recognizer()


def record_text():
    """Record text from microphone"""
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("Listening...")
                audio2 = r.listen(source2)
                my_text = r.recognize_google(audio2)
                return my_text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")


def send_to_gpt(messages, model="gpt-3.5-turbo"):
    """Send text to GPT-3 and return response"""
    resp = client.completions.create(
        model=model,
        prompt=messages,
        stop=None,
        temperature=0.5,
        max_tokens=100
    )

    message = resp.choices[0].message.content
    messages.append(resp.choices[0].message)
    return message


messages = [{"role": "user", "content": "Please act like JARVIS from Iron Man."}]
while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_gpt(messages)
    speak_text(response)
    print(response)
