import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your-NewsAPI-Key>"
openai_key = "<Your-OpenAI-Key>"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text, lang='en', tld='com')  # tld='com' gives a modern US voice
    tts.save('temp.mp3') 

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "You are Juno — a super-intelligent, modern, confident assistant. You respond with short, sharp, helpful, and slightly witty answers like a tech-savvy best friend."
            },
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Launching Google.")
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        speak("Taking you to Facebook.")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        speak("Let’s dive into YouTube.")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        speak("Opening LinkedIn. Time to look professional.")
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        try:
            song = c.split(" ")[1]
            link = musicLibrary.music[song]
            speak(f"Playing {song} for you.")
            webbrowser.open(link)
        except Exception as e:
            speak("Hmm, that song isn't in my list.")
            print(e)

    elif "news" in c:
        speak("Let me fetch some fresh headlines for you.")
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles[:5]:  # Limit to 5 headlines
                    speak(article['title'])
        except:
            speak("Oops. Couldn't fetch the news right now.")
    else:
        speak("Thinking...")
        response = aiProcess(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Juno. Ready to roll.")
    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "juno":
                speak("Yes? I'm listening.")
                with sr.Microphone() as source:
                    print("Juno Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error:", e)
