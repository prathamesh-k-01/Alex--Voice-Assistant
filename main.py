import pyttsx3
import speech_recognition as sr
import datetime
import subprocess, sys
import webbrowser
import wikipedia
import pywhatkit as kit
import time
import json
import requests
import wolframalpha
import re
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)

# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

#Wolframalpha api
try:
    app_id = "39QAQK-XTPWUPJVP6"
    client = wolframalpha.Client(app_id)
except Exception:
    speak("Error")

# voice to text
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source,1.2)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "none"
    return query

# to wish
def wish():
    hour=datetime.datetime.now().hour
    if hour>=3 and hour<12:
        speak("Hello,Good Morning")

    elif hour>=12 and hour<16:
        speak("Hello,Good Afternoon")

    else :
        speak("Hello,Good Evening")
    speak("I am Alex, your assistant. Please tell me how can i help you?")

if __name__ == "__main__":
    wish()
    while True:
        query1 = takeCommand().lower()
        # logic building for tasks

        if 'launch app' in query1:
            speak("Which app u want to launch")
            app = takeCommand().lower()
            npath = "C://Users//sameep//Desktop//New folder//" + app
            os.startfile(npath)
            # os.system("open /Applications/Google\ Chrome.app")

        """if 'launch' in query1:
            reg_ex = re.search('launch (.*)', query1)
            if reg_ex:
                appname = reg_ex.group(1)
                appname1 = appname.replace(" ", "\ ")
                os.system("open -a " + appname1)
                speak('Launching ' + appname)"""

        if 'open' in query1:
            reg_ex = re.search('open (.*)', query1)
            if reg_ex:
                domain = reg_ex.group(1)+".com"
                print(domain)
                url = 'https://www.' + domain
                webbrowser.open(url)
                speak('The website you have requested has been opened for you Sir.')
            else:
                pass

        elif 'hello' in query1:
            speak("Hello I am Alex, your desktop assistant")

        elif 'wikipedia' in query1:
            speak("Searching Wikipedia...")
            query1 = query1.replace("wikipedia", "")
            results = wikipedia.summary(query1, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query1:
            speak("Opening YouTube...")
            webbrowser.open('https://www.youtube.com/', new=2)

        elif 'open google' in query1:
            speak("Opening google...")
            webbrowser.open('https://www.google.com/', new=2)

        elif "play song on youtube" in query1:
            speak("which song you want me to play for you?")
            song = takeCommand().lower()
            speak("playing " + song)
            kit.playonyt(song)
            time.sleep(5)

        elif "youtube" in query1:
            speak("Opening YouTube...")
            query1 = query1.replace("youtube", "")
            kit.playonyt(query1)
            time.sleep(5)

        elif 'google' in query1:
            speak("Opening Google...")
            query1 = query1.replace("google", "")
            kit.search(query1)
            time.sleep(5)

        elif query1=="what is the time" or query1=="what time is it" :
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open gmail' in query1:
            webbrowser.open('https://www.gmail.com/', new=2)
            speak("Google Mail open now")
            time.sleep(5)

        elif 'search' in query1:
            query1 = query1.replace("search", "")
            kit.search(query1)
            time.sleep(5)

        elif 'news' in query1:
            news = webbrowser.open("https://timesofindia.indiatimes.com/home/headlines", new=2)
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif "joke" in query1:
            res = requests.get('https://icanhazdadjoke.com/',
                headers={"Accept": "application/json"})
            if res.status_code == requests.codes.ok:
                speak(str(res.json()['joke']))
            else:
                speak('oops!I ran out of jokes')

        elif 'ask' in query1:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question = takeCommand().lower()
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)

        elif 'temperature' in query1:
            res = client.query(query1)
            answer = next(res.results).text
            speak(answer)

        elif 'capital' in query1 and 'of' in query1:
            res = client.query(query1)
            answer = next(res.results).text
            speak(answer)

        elif "weather" in query1:
            api_key = "b809b4499aa3c69460984f194dde3a91"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the region name")
            city_name = takeCommand()
            while city_name=="none":
                city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404" and city_name!="none":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                temp = current_temperature - 273.15
                speak(" Temperature in "+city_name+" in celcius unit is " +
                      str(round(temp,2)) + "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n and the weather can be described as " +
                      str(weather_description))
            else:
                speak(" City Not Found ")

        elif 'exit' in query1 or "good bye" in query1 or "bye" in query1 or "stop" in query1 or'quit' in query1 or 'abort' in query1:
            speak("Thanks for giving me your time")
            break

        elif query1 == 'none':
            continue

        else:
            try:
                res = client.query(query1)
                answer = next(res.results).text
                speak(answer)
            except Exception as e1:
                temp1 = query1.replace(' ', '+')
                g_url = "https://www.google.com/search?q="
                speak("Sorry. I am not Sure I understand but here are the web results")
                webbrowser.open(g_url+temp1, new=2)

