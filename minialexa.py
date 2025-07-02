import os
import pygame
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
from pytube import YouTube

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
    except Exception:
        print("Sorry, I didn't catch that.")
        return "None"
    return query.lower()

def download_and_play_youtube_audio(search_query, music_dir):
    try:
        from pytube import Search
        s = Search(search_query)
        yt = s.results[0]
        speak(f"Downloading and playing {yt.title}")
        stream = yt.streams.filter(only_audio=True).first()
        output_file = stream.download(output_path=music_dir, filename="online_song.mp3")
        return output_file
    except Exception as e:
        speak("Sorry, I couldn't download the song.")
        print(e)
        return None

def main():
    wish_user()

    pygame.mixer.init()
    is_music_playing = False
    volume = 0.5
    pygame.mixer.music.set_volume(volume)

    music_dir = r"C:\projects\alexa\music"

    while True:
        query = take_command()

        if 'time' in query:
            speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print("According to Wikipedia")
                speak(result)
            except wikipedia.DisambiguationError as e:
                speak(f"The topic '{query}' is too ambiguous.")
                print(e.options[:5])
            except wikipedia.PageError:
                speak("Page not found.")
            except Exception as e:
                speak("Error searching Wikipedia.")
                print(e)

        elif 'play' in query or 'song' in query:
            songs = os.listdir(music_dir)
            if songs:
                song_path = os.path.join(music_dir, songs[0])
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                speak(f"Playing: {songs[0]}")
                is_music_playing = True
            else:
                speak("No local songs found.")

        elif 'pause' in query and is_music_playing:
            pygame.mixer.music.pause()
            speak("Music paused.")

        elif 'resume' in query and is_music_playing:
            pygame.mixer.music.unpause()
            speak("Resuming music.")

        elif 'volume up' in query or 'increase volume' in query:
            if volume < 1.0:
                volume = min(1.0, volume + 0.1)
                pygame.mixer.music.set_volume(volume)
                speak(f"Volume increased to {int(volume * 100)} percent.")
            else:
                speak("Volume is already at maximum.")

        elif 'volume down' in query or 'decrease volume' in query:
            if volume > 0.0:
                volume = max(0.0, volume - 0.1)
                pygame.mixer.music.set_volume(volume)
                speak(f"Volume decreased to {int(volume * 100)} percent.")
            else:
                speak("Volume is already at minimum.")

        elif 'play online' in query or 'online song' in query:
            song_name = query.replace("play online", "").replace("online song", "").strip()
            file_path = download_and_play_youtube_audio(song_name, music_dir)
            if file_path:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                is_music_playing = True

        elif 'open portfolio' in query:
            speak("Opening portfolio...")
            webbrowser.open("https://bramhendra-protofolio.netlify.app/")

        elif 'youtube' in query:
            q = query.replace("search", "").replace("youtube", "").strip()
            if not q:
                speak("What should I search on YouTube?")
                q = take_command()
            if q and q != "None":
                speak(f"Searching YouTube for {q}")
                webbrowser.open(f"https://www.youtube.com/results?search_query={q}")

        elif 'search' in query or 'google' in query:
            q = query.replace("search", "").replace("google", "").strip()
            speak(f"Searching Google for {q}")
            webbrowser.open(f"https://www.google.com/search?q={q}")

        elif 'exit' in query or 'stop' in query or 'bye' in query:
            speak("Bye! Have a nice day.")
            break

if __name__ == "__main__":
    main()
