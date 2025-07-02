import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit as kit


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception as e:
        print("Sorry, I didn't catch that.")
        return "None"
    return query.lower()

def main():
    wish_user()
    while True:
        query = take_command()

        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()

            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print("According to Wikipedia")
                speak(result)

            except wikipedia.DisambiguationError as e:
                speak(f"The topic '{query}' is too ambiguous. Please be more specific.")
                print(f"Disambiguation options: {e.options[:5]}") 

            except wikipedia.PageError:
                speak("Sorry, I couldn't find any page matching your query.")

            except Exception as e:
                speak("Something went wrong while searching Wikipedia.")
                print(e)
        elif 'play' in query or 'song' in query:
            song = query.replace('play', '').strip()
            speak(f"Playing {song} on YouTube")
            kit.playonyt(song)
        
        elif 'open  portfolio' in query:
            speak("Wait! , opening protofolio...")
            webbrowser.open("https://bramhendra-protofolio.netlify.app/")
        
        elif 'youtube' in query:
            query = query.replace("search", "").replace("youtube", "").strip()
            if not query:
                speak("What should I search on YouTube?")
                query = take_command()

            if query and query != "None":
                speak(f"Searching YouTube for {query}")
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        elif 'search' in query or 'google' in query:
            query = query.replace("search", "").replace("google", "").strip()
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        
        elif 'exit' in query or 'stop' in query or 'bye' in query:
            speak("bye! , Have a nice day")
            break


if __name__ == "__main__":
    main()