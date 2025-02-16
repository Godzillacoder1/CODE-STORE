import wikipedia  # For fetching information from Wikipedia
import pywhatkit as kit  # To automate tasks (like playing YouTube videos, etc.)
import webbrowser
import pyjokes
import re
import pyttsx3  # For text-to-speech
import speech_recognition as sr  # For speech recognition
import sounddevice as sd  # For audio input
import numpy as np
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to make the AI speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to listen to the user's voice input using sounddevice and speechrecognition
def listen():
    recognizer = sr.Recognizer()

    # Record audio using sounddevice
    with sd.InputStream(samplerate=16000, channels=1, dtype='int16') as stream:
        print("Listening...")
        audio_data = np.array([])  # Initialize empty array to store the audio data
        for _ in range(0, int(16000 / 1024 * 5)):  # Capture 5 seconds of audio
            block, overflowed = stream.read(1024)  # Read a block of audio
            audio_data = np.append(audio_data, block)  # Append to the audio data array

    # Convert audio data to AudioData for recognition
    audio = sr.AudioData(audio_data.tobytes(), 16000, 2)

    try:
        query = recognizer.recognize_google(audio).lower()
        print(f"You said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        query = listen()  # Retry if no voice is recognized
    except sr.RequestError:
        speak("Sorry, I'm having trouble with the speech service.")
        query = None
    return query


# Function to handle Jarvis commands
def jarvis():
    speak("Hello, Great Emperor Aansh")

    while True:
        query = listen()  # Listen for user input

        # Command to exit the loop
        if query and ("exit" in query or "quit" in query):
            speak("See you again, sir.")
            break

        # Tell a joke
        elif query and "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Get a Wikipedia summary for a query
        elif query and ("what is" in query or "who is" in query):
            speak("Searching Wikipedia...")
            query = query.replace("what is", "").replace("who is", "")
            try:
                summary = wikipedia.summary(query, sentences=1)
                speak(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Can you be more specific? I found multiple results: {e.options}")
            except wikipedia.exceptions.HTTPTimeoutError:
                speak("Sorry, I couldn't fetch the information right now.")

        # Open YouTube
        elif query and "open youtube" in query:
            url = 'https://www.youtube.com'
            webbrowser.open(url)

        # Search Google for a query
        elif query and "search" in query:
            speak("Searching Google...")
            query = query.replace("search", "")
            kit.search(query)

        # Play music on YouTube
        elif query and "play music" in query:
            speak("Playing music for you...")
            kit.playonyt("music")

        # Tell the current time
        elif query and "what time is it" in query:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        # Greet the user
        elif query and "hello" in query:
            speak("Hello! How can I assist you today?")

        # Calculations
        elif query and ("calculate" in query or "what is" in query):
            expression = re.sub(r"[^0-9\*-+/.]", "", query)
            try:
                result = eval(expression)
                speak(f"The result is {result}")
            except Exception as e:
                speak(f"Sorry, I couldn't catch that. Please rephrase. Error: {e}")

        # Play a game (Snake game)
        elif query and (
                "play game" in query or "games" in query or "I wanna play a game" in query or "I feel bored" in query):
            url = 'https://snake.googlemaps.com/'
            webbrowser.open(url)

        # Handle unknown commands
        else:
            speak("Mind rephrasing that, sir?")


# Run Jarvis
jarvis()
