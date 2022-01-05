from __future__ import print_function
import webbrowser

import speech_recognition
import pyttsx3
import time
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pprint

engine = pyttsx3.init()
webbrowser.register('chrome', None)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

search_api_key = ''
cse_id = ''

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def computerTime():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(Time)

def events():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Events for today')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        speak(start)
        speak(event['summary'])

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

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def actions():
    statement = takeCommand().lower()
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
    if 'news' in statement:
        webbrowser.open_new_tab("https://www.bbc.com")
        speak('Here are some headlines from BBC')
        time.sleep(6)
    if 'time' in statement:
        computerTime()
    if 'calendar' in statement:
        events()
    if 'open chapter website' in statement:
        webbrowser.open_new_tab("pksbetachi.org")
        speak("Opening Beta Chi website")
        time.sleep(5)
    if 'Phi Kappa Sigma website' in statement:
        webbrowser.open_new_tab("pks.org")
        speak("Opening Phi Kap's national website")
        time.sleep(5)
    else:
        results = google_search(statement, search_api_key, cse_id)
        count = 0;
        for results in results:
            count += 1
            speak('top search result was on ' + results['link'])
            speak(results['snippet'])
            if count == 1:
                break

if __name__=="__main__":
    while True:
        statement = wakeCommand().lower()
        if "hey atlas" in statement:
            speak("How many I assist you")
            actions()
