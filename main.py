import datetime
import webbrowser
import speech_recognition
import pyttsx3
import wikipedia
import time


engine = pyttsx3.init()
webbrowser.register('chrome', None)
first = True

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def computerTime():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(Time)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    stringMonth = ""
    if month == 1:
        stringMonth = "January"
    elif month == 2:
        stringMonth = "February"
    elif month == 3:
        stringMonth = "March"
    elif month == 4:
        stringMonth = "April"
    elif month == 5:
        stringMonth = "May"
    elif month == 6:
        stringMonth = "June"
    elif month == 7:
        stringMonth = "July"
    elif month == 8:
        stringMonth = "August"
    elif month == 9:
        stringMonth = "September"
    elif month == 10:
        stringMonth = "October"
    elif month == 11:
        stringMonth = "November"
    elif month == 12:
        stringMonth = "December"

    speak(stringMonth)
    speak(day)
    speak(year)

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        speak("Say that again please")

        return "None"
    return query

def wakeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        return "None"
    return query

def actions():
    statement = takeCommand().lower()
    if 'wikipedia' in statement:
        speak('Searching Wikipedia...')
        statement = statement.replace("wikipedia", "")
        results = wikipedia.summary(statement, sentences=3)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    if 'open youtube' in statement:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("youtube is open now")
        time.sleep(5)
    if 'open google' in statement:
        webbrowser.open_new_tab("https://www.google.com")
        speak("Google chrome is open now")
        time.sleep(5)
    if 'open gmail' in statement:
        webbrowser.open_new_tab("gmail.com")
        speak("Google Mail open now")
        time.sleep(5)
    if 'time' in statement:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"the time is {strTime}")
    if 'news' in statement:
        webbrowser.open_new_tab("https://www.cnn.com")
        speak('Here are some headlines from cnn,Happy reading')
        time.sleep(6)
    if 'time' in statement:
        computerTime()

if __name__=="__main__":
    while True:
        statement = wakeCommand().lower()
        if "hey atlas" in statement:
            speak("How many I assist you")
            actions()