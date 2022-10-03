import time
from tkinter import *
import speech_recognition as sr
import os
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyttsx3
import datetime
import webbrowser
import wikipedia


def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voice')
    engine.setProperty('voice', voices[1])
    engine.setProperty('rate', 180)
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
        en1.set("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
        en1.set("Good Afternoon")
    else:
        speak("Good Evening!")
        en1.set("Good Evening")
    speak("Hello sir I am zo how may i help you")
    screen.update()


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening...")
        en1.set("Listening...")
        screen.update()
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        # print("Recognizing...")
        en1.set("Recognizing...")
        screen.update()
        query = r.recognize_google(audio, language='en-in')
        # print(f"User said: {query}\n")
        en1.set(f"User said: {query}\n")
        screen.update()

    except Exception as e:

        speak("Say that again please...")
        en1.set("Say that again please...")
        screen.update()
        return "None"
    screen.update()
    return query


def camera():
    import cv2
    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()


def play_video(song_name):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    links = []

    # Open YouTube page for each search term
    driver.get('https://www.youtube.com/results?search_query={}'.format(song_name))
    # Find a first webelement with video thumbnail on the page
    link_webelement = driver.find_element(By.CSS_SELECTOR,
                                          'div#contents ytd-item-section-renderer>div#contents a#thumbnail')
    # Grab webelement's href, this is your link, and store in a list of links:
    links += [link_webelement.get_attribute('href')]

    webbrowser.open(links[0])
    time.sleep(5)


def coronaupdatr():
    global en2, screen
    from bs4 import BeautifulSoup
    import requests
    import html5lib

    url = "https://www.worldometers.info/coronavirus/country/india/"
    r = requests.get(url).text

    # print(htmlcontent)
    soup = BeautifulSoup(r, 'html.parser')
    prefix = ["Total Cases are:-", "Deaths are:-", "Recovered are:-"]
    res = ""
    values = soup.find_all("div", {"class": "maincounter-number"})
    for i in range(len(values)):
        res += prefix[i] + values[i].get_text().strip() + " ,"
    speak(res)
    en2.set(res)
    Result.update()


# reaction on command
def say():
    en2.set("")
    Result.update()
    query = takeCommand().lower()

    if 'hi' == query:
        speak("Sorry something is wrong ")
        en2.set("Sorry something is wrong")
        Result.update()

    elif "volume" in query:
        if "up" in query or "down" in query:
            speak("By how many times?")
            en2.set("By how many times?")
            try:
                for i in range(int(takeCommand())):
                    if "up" in query:
                        pyautogui.press("volumeup")
                        en2.set("Done!")
                    elif "down" in query:
                        pyautogui.press("volumedown")
                        en2.set("Done!")
            except:
                speak("Try again")
                en2.set("Try Again!!")
        elif "mute" in query:
            pyautogui.press("volumemute")

    elif 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        en2.set(results)
        Result.update()

    elif 'open google' in query:
        webbrowser.open("google.com")
        en2.set("Opening Google")
        speak("Opening Google")
        Result.update()

    elif 'open stack overflow' in query:
        webbrowser.open("stackoverflow.com")
        en2.set("Opening Stackover flow")
        speak("Opening Stack over flow")
        Result.update()

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")
        en2.set(f"Sir, the time is {strTime}")
        Result.update()

    elif 'covid update' in query:
        coronaupdatr()

    elif 'open web browser' in query:
        speak("Oening Microsotf Edge")
        en2.set("Oening Microsotf Edge")
        Result.update()
        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')

    elif 'lock' in query:
        speak("locking your pc")
        os.system("shutdown/l")

    elif "restart" in query:
        speak("Restarting PC")
        os.system("shutdown /r /t 01")

    elif "shutdown" in query:
        speak("Shutting down PC")
        os.system("shutdown /s /t 01")

    elif " Google meet" in query:
        webbrowser.open('https://meet.google.com/')
        speak("opening Google meet")

    elif '.com' in query:
        query = query.replace("open", "")
        speak(f"opening {query}")
        en2.set(f"opening {query}")
        webbrowser.open(query)

    elif '.in' in query:
        query = query.replace("open", "")
        speak(f"opening {query}")
        en2.set(f"opening {query}")
        webbrowser.open(query)

    elif 'who made you' in query:
        en2.set("Mr.Hardik made me")
        speak("Mr.Hardik made me")

    elif "search" in query:
        en2.set("Searching Google")
        speak("Searching Google")
        new = 2
        tabUrl = "http://google.com/search?q="
        term = query.replace("search", "")
        webbrowser.open(tabUrl + term, new=new)

    elif "play" in query:
        query = query.replace("play", "")
        try:
            speak(f"Playing{query}")
            en2.set(f"Playing{query}")
            Result.update()
            play_video(query)

        except IndexError as e:
            print(e)
            speak(f"OOPs, can't find{query}")
            en2.set(f"OOPs, can't find{query}")
            Result.update()

    elif "screenshot" in query:
        time_ = datetime.datetime.now().strftime("%H:%M:%S").replace(":", ".")
        pyautogui.hotkey('alt', 'tab')
        en2.set(f"Screenshot taken with filename:-{time_}")
        speak(f"Screenshot taken with filename {time_}")
        pyautogui.screenshot().save(f"{time_}.png")

    elif "camera" in query:
        en2.set("opening Camera")
        speak("opening camera")
        camera()

    elif "close" in query:
        pyautogui.hotkey('alt', 'tab')
        pyautogui.hotkey('alt', 'f4')
        speak("Alternate program closed")
        en2.set("Alternate program closed")

    elif "run" in query:
        if "pycharm" in query:
            speak("Opening Pycharm")
            en2.set("Opening Pycharm")
            os.system(r'"C:/Program Files/JetBrains/PyCharm Community Edition 2021.3.2/bin/pycharm64.exe"')
        # todo: adding apps
        # elif "streamlab" in query:
        #     speak("Opening Streamlabs")
        #     en2.set("Opening Streamlabs")
        #     os.system('"G:\Stream Lab\Streamlabs OBS.exe"')

        # elif "vs code" in query:
        #     speak("Opening Visiual Studio code")
        #     en2.set("Opening Visiual Studio code")
        #     os.system(r'"C:\Users\{0}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getlogin())')

    elif "help" in query:
        #todo: making help box
        pass
    else:
        speak("Please use proper keyword. say \"help\" to see all keywords")
        en2.set("Please use proper keyword. say \"help\" to see all keywords")
# GUI
root = Tk()
root.configure(bg="#aaccbb")
root.title("Zo - Hardik")
root.geometry("600x400")
f1 = Frame(root, relief=RIDGE, bg="Black", borderwidth=8)
f1.pack(padx=10, pady=5)
text = Label(f1, text="ZO", font="monotype 42", bg="black", fg="White")
root.iconphoto(False, PhotoImage(file='ai.png'))
text.pack()
en1 = StringVar()
en1.set("")
screen = Entry(root, textvariable=en1, font="lucica 20 bold")
screen.pack(fill=X, padx=5, pady=5)

Button(text="Speak", font="lucica 20 bold", command=say).pack(padx=5, pady=5)
en2 = StringVar()
en2.set("")
Result = Entry(root, textvariable=en2, font="lucica 16 bold")
Result.pack(fill=BOTH, padx=5, pady=5)

wishMe()

root.mainloop()
