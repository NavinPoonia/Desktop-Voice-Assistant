import os
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import _thread
from plyer import notification
from bs4 import BeautifulSoup
import requests
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


def Speak(audio):
    engine.say(audio)
    engine.runAndWait()


def WishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        Speak('Good Morning!')
    elif hour >= 12 and hour < 18:
        Speak('Good Afternoon!')
    else:
        Speak('Good Evening!')

    Speak('I am Jarvis. How can I help you')


def takeCommand():
    """It takes microphone input from the user and returns string output"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('\nListening....\n')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing....\n')
        query = r.recognize_google(audio, language="en-in")
        print(f"User said : {query}\n")

    except Exception as e:
        print("Say that again Please")
        return "None"

    return query


def notifyMe(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon="E:\programming\Python projects\Corona Notification\icon_PUV_icon.ico",
        timeout=5,
    )


def getData(url):
    r = requests.get(url)
    return r.text


if __name__ == "__main__":
    WishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing Task based on query
        if 'wikipedia' in query:
            Speak('searching wikipedia.....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            Speak("According to Wikipedia")
            print(results)
            Speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")


        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'music' in query:
            Speak('whom Do you want to listen. Justin Bieber or Eminem. some relaxing Music will be good . you must take break ')
            music_dir = "E:\programming\Python projects\Jarvis AI Assistant\songs"
            songs = os.listdir(music_dir)
            song_name = takeCommand().lower()
            if 'justin' in song_name:
                os.startfile(os.path.join(music_dir, songs[0]))
            elif 'eminem' in song_name:
                os.startfile(os.path.join(music_dir, songs[1]))
            elif 'relax' in song_name:
                os.startfile(os.path.join(music_dir, songs[2]))
            else:
                Speak('Relax Buddy')
                os.startfile(os.path.join(music_dir, songs[2]))

        elif 'alarm' in query:
            Speak('set the time sir')
            time_Hours = int(input("Set Hour :"))
            time_Minutes = int(input(('Set The Minutes :')))

            def thread_alarm():
                while True:
                    if datetime.datetime.now().hour == time_Hours and datetime.datetime.now().minute == time_Minutes:
                        music_dir = "E:\programming\Python projects\Jarvis AI Assistant\songs"
                        songs = os.listdir(music_dir)
                        os.startfile(os.path.join(music_dir, songs[2]))
                        break

            _thread.start_new_thread(thread_alarm, ())

        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            Speak(f"sir ,The time is {strtime}")
            print(strtime)

        elif 'open code' in query:
            codepath = "C:\\Users\\Navin\\AppData\\Local\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)

        elif 'notify' in query:
            myHtmlData = getData("https://prsindia.org/covid-19/cases")
            soup = BeautifulSoup(myHtmlData, 'html.parser')

            for tr in soup.table.tbody.find_all('tr'):
                str = ""
                for td in tr:
                    str += f"{td.get_text()},"

                list = str.split(',')

                while ("" in list):
                    list.remove("")

                # you can add states you want to get notified
                states = ['Haryana', 'Maharashtra']
                for item in states:
                    if item == list[1]:
                        print(list)
                        title = 'Cases of Corona'
                        message = f"{item} \nConfirmed: {list[2]}\nActive: {list[3]}, Cured: {list[4]}\nDeaths: {list[5]}"
                        notifyMe(title, message)
                        time.sleep(10)

        elif 'map' in query:
            webbrowser.open("https://navinpoonia.github.io/Plotting%20Corona%20Cases%20on%20World%20Map/")

        elif 'speech' in query:
            webbrowser.open("https://navinpoonia.github.io/Speech%20To%20Text%20Recognition/");


        elif 'bye' in query:
            Speak('Thanks Buddy Goodbye')
            exit()

        else:
            continue
