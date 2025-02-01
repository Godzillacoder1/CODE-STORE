import wikipedia  # For fetching information from Wikipedia
import pywhatkit as kit  # To automate tasks (like playing YouTube videos, etc.)
import webbrowser
import pyjokes
import re

# Function to make the AI speak (this time we'll just print the response)
def speak(text):
    print(f"Jarvis: {text}")


# Function to handle Jarvis commands
def jarvis():
    speak("Hello, Great Emporer Aansh")

    while True:
        # Get user input (text-based commands)
        query = input("You: ").lower()

        # Command to exit the loop
        if "exit" in query or "quit" in query:
            speak("See you again sir")
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

        # Open YouTube search
        elif "open youtube" in query:
            url = 'https://www.youtube.com'

            # open it
            webbrowser.open(url)
        # Default to opening YouTube; can be customized for specific searches

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
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        # Greet the user
        elif "hello" in query:
            speak("Hello! How can I assist you today?")
        #calctuins
        elif "calculate" in query or "what is" in query:
            expression = re.sub(r"[^0-9\*-+/.]","",query)
            try:
                result = eval(expression)
                speak(f"the result is {result}")
            except Exception as e:
                speak(f"sorry could catch that please rephrase. Error: {e}")
        # games
        elif "play game" in query  or "games" in query or "I wanna play a game" in query or "I feel bored" in query:
            url = 'https://snake.googlemaps.com/'

            # Open URL in the default browser
            webbrowser.open(url)


        # Handle unknown commands
        else:
            speak("Mind reprasing that sir?")


# Run Jarvis
jarvis()
