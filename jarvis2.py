import wikipedia  # For fetching information from Wikipedia
import pywhatkit as kit  # To automate tasks (like playing YouTube videos, etc.)
import webbrowser
import pyjokes
import re
import pyttsx3  # For text-to-speech
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to make the AI speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle Jarvis commands
def jarvis():
    speak("Hello, Great Emperor Aansh")

    while True:
        # Get user input (text-based commands)
        query = input("You: ").lower()

        # Command to exit the loop
        if "exit" in query or "quit" in query:
            speak("See you again, sir.")
            break

        # Tell a joke
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Get a Wikipedia summary for a query
        elif "what is" in query or "who is" in query:
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
        elif "open youtube" in query:
            url = 'https://www.youtube.com'
            webbrowser.open(url)

        # Search Google for a query
        elif "search" in query:
            speak("Searching Google...")
            query = query.replace("search", "")
            kit.search(query)

        # Play music on YouTube
        elif "play music" in query:
            speak("Playing music for you...")
            kit.playonyt("music")

        # Tell the current time
        elif "what time is it" in query:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        # Greet the user
        elif "hello" in query:
            speak("Hello! How can I assist you today?")

        # Calculations
        elif "calculate" in query or "what is" in query:
            expression = re.sub(r"[^0-9\*-+/.]", "", query)
            try:
                result = eval(expression)
                speak(f"The result is {result}")
            except Exception as e:
                speak(f"Sorry, I couldn't catch that. Please rephrase. Error: {e}")

        # Play a game (Snake game)
        elif "play game" in query or "games" in query or "I wanna play a game" in query or "I feel bored" in query:
            url = 'https://snake.googlemaps.com/'
            webbrowser.open(url)

        # Handle unknown commands
        else:
            speak("Mind rephrasing that, sir?")

# Run Jarvis
jarvis()
