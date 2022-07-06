from xml.dom import NotFoundErr
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import datetime
import requests
import pyttsx3  # text to speech
import speech_recognition as sr  # speech to text
import smtplib
import webbrowser
import os
import sys
import wikipedia
import threading
import json
import PyPDF2

from simple_image_download import simple_image_download as sim
from configparser import ConfigParser
from threading import Timer
from tkinter import *
from pygame import mixer

import pyaudio
import numpy as np

# Custom Packages
import sysInfo
import setReminder

from chatBot import chatBot


config = ConfigParser()
config.read('config.ini')
weatherAPI_key = config['weather_api']['weather_key']
newsAPI_key = config['news_api']['news_key']

newsUrl = 'https://newsapi.org/v2/top-headlines?country=in&apiKey='
weatherUrl = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

maxValue = 2 ** 16
bars = 10
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=2,
                rate=44100, input=True, frames_per_buffer=1024)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)0
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)
mixer.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("Sir, I am your Voice Assistant . Please tell me how may I help you")
    # widget.userText("Sir, I am your Voice Assistant . Please tell me how may I help you")


class PassDataSignals(QObject):
    get_text_signal = pyqtSignal(str)
    get_image_signal = pyqtSignal(str)
    get_active_widget = pyqtSignal(str)


dataSignals = PassDataSignals()


def setCommandText(text):
    dataSignals.get_text_signal.emit(text)


def setPixmap(img):
    dataSignals.get_image_signal.emit(img)


def setWidget(text):
    dataSignals.get_active_widget.emit(text)

def image_search(query):
    try:
        response = sim.simple_image_download
        response().download(query, 1)
    except Exception as e:
        print('Download Problem', e)


def get_weather(city):
    result = requests.get(weatherUrl.format(city, weatherAPI_key))
    if result:
        result_json = result.json()
        city = result_json['name']
        country = result_json['sys']['country']
        temp_kelvin = result_json['main']['temp']
        temp_celsius = round(temp_kelvin - 273.15)
        icon = result_json['weather'][0]['icon']
        weather = result_json['weather'][0]['main']
        final_result = (city, country, temp_celsius, icon, weather)
        return final_result
    else:
        return None


def getNews():
    try:
        requests_url = requests.get(newsUrl + newsAPI_key)
        # print(requests_url)
        news_data = json.loads(requests_url.content)
        # print(news_data)
        # one articles
        # print(get_news)

        numberOfNews = 2
        for i in range(numberOfNews):

            get_news = news_data['articles'][i]['title']

            # image download
            news_image = news_data['articles'][i]['urlToImage']
            response = requests.get(news_image)
            file = open(".\\news_images\\news_image.jpg", "wb")
            file.write(response.content)
            file.close()

            image = os.listdir(f'.\\news_images')
            setWidget("Result")
            setPixmap(f'.\\news_images\\' + image[0])

            setCommandText(get_news)
            print(get_news)
            speak(get_news)

            if i < (numberOfNews - 1):
                speak("Moving on to the next news..")
                print("Moving on to the next news..")

    except Exception as e:
        print(e)

    setPixmap('')
    setCommandText("Thanks for listening...")
    speak("Thanks for listening...")
    print("Thanks for listening...")


def takeCommand(time_taken):
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        setCommandText("Listening...")
        setWidget("Listening")

        audio = r.listen(source, phrase_time_limit=time_taken)

    try:
        print("Recognizing...")
        setCommandText("Recognizing...")
        setWidget("Recognizing")

        query = r.recognize_google(audio, language='en-in')
        setCommandText(query)
        print(f"User said: {query}\n")
        setWidget("")

    except Exception as e:
        print(e)
        print("Say that again please...")
        return "voice problem"

    query = query.lower()
    return query


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.executeCommands()

    def executeCommands(self):
        self.query = takeCommand(5)
        self.query = self.query.lower()

        if 'the time' in self.query or 'time' in self.query or 'tell me time' in self.query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            setCommandText(f"Sir, the time is {strTime}")

        # Google
        elif 'open google' in self.query or "google search" in self.query:
            self.url = "https://www.google.com/"
            self.getSearch = self.query.replace("google search ", "")
            self.googleSearch = self.getSearch.replace(" ", "+")

            speak("Ok")

            if 'open google' in self.query:
                webbrowser.open(self.url)
            elif "google search" in self.query:
                webbrowser.open(self.url + "search?q=" + self.googleSearch)

                speak("Here is Search Result from Google")

        elif 'open drive' in self.query:
            self.url = "https://drive.google.com/"
            webbrowser.open(self.url)

        elif 'open mail' in self.query:
            self.url = "https://mail.google.com/mail/u/0/#inbox"
            webbrowser.open(self.url)

        elif 'open youtube' in self.query or "youtube search" in self.query:
            self.url = "https://www.youtube.com/"
            self.sortQuery = self.query.replace('open youtube', '')
            self.searchQuery = self.query.replace('youtube search', '')
            self.getFeed = self.sortQuery.replace(' ', '')

            if 'search' in self.sortQuery:
                webbrowser.open(
                    self.url + "results?search_query=" + self.searchQuery)
                speak("Here is Search Result from Youtube")

            elif self.sortQuery != '':
                webbrowser.open(self.url + "feed/" + self.getFeed)

            else:
                webbrowser.open(self.url)

        elif 'open github' in self.query or 'github search' in self.query:
            self.url = "https://www.github.com/"
            webbrowser.open(self.url)

        elif 'open stackoverflow' in self.query or 'open stack overflow' in self.query:
            self.url = "https://www.stackoverflow.com/"
            webbrowser.open(self.url)

        elif 'open w3school' in self.query:
            self.url = "https://www.w3schools.com/"
            webbrowser.open(self.url)

        elif 'open geeksforgeeks' in self.query or 'open geeks for geeks' in self.query:
            self.url = "https://www.geeksforgeeks.org/"
            self.searchQuery = self.query.replace("open geeksforgeeks", "")
            self.searchQuery = self.query.replace("open geeks for geeks", "")
            self.getCourse = self.searchQuery[1:]
            self.getCourse = self.getCourse.replace(" ", "-")
            print(self.searchQuery)

            if self.searchQuery != "":
                webbrowser.open("https://www.geeksforgeeks.org/" +
                                self.getCourse + "/?ref=shm")
            else:
                webbrowser.open(self.url)

        elif 'open chrome' in self.query:
            speak('ok')
            openApp = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            os.startfile(openApp)

        elif 'play music' in self.query:
            music_dir = r'G:\music'
            songs = os.listdir(music_dir)
            # print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
            setCommandText('Okay, here is your music!\n\tEnjoy!')
            speak('Okay, here is your music!\nEnjoy!')
            print('Okay, here is your music!\nEnjoy!')

        elif 'tell me news' in self.query:
            getNews()

        elif 'read file' in self.query:

            # setWidget
            print("Select file to read")
            speak("Select file to read")
            defaultPath = r"C:\Users\gajal\Desktop\Voice Assistant 2.0 - Copy"

            try:
                showWidget = QWidget()
                getFile = QFileDialog.getOpenFileNames(
                    showWidget, 'Select File to Read', defaultPath, 'Text Files (*.pdf *.doc *.txt)')
                showWidget.show()
                showWidget.close()

                file = getFile[0][0]
                print("Selected File:", file)

                splitFile = os.path.splitext(file)
                fileExtension = splitFile[1]

                if fileExtension == '.pdf':
                    pdfReader = PyPDF2.PdfFileReader(getFile[0][0])
                    page = pdfReader.getPage(1)
                    textRead = page.extractText()
                    speak(textRead)
                elif fileExtension == '.txt':
                    readFile = open(file, 'r')
                    readText = readFile.read()
                    speak(readText)

            except Exception:
                print("File not Selected")
                speak("File not Selected")

        elif 'set reminder' in self.query or 'set a reminder' in self.query:

            speak("What is reminder")
            self.getReminder = takeCommand(5)
            speak("In Which Day do you want to set reminder")
            self.getDay = takeCommand(2)
            speak("What is time of reminder")
            self.getTime = takeCommand(2)

            if self.getDay == 'today':
                setReminder.setReminderAt(self.getReminder, self.getTime)
            else:
                print("Another Day")
                setReminder.setReminderOn(
                    self.getReminder, self.getDay, self.getTime)

            speak("reminder set Successful")
            setCommandText("reminder set Successful")

        elif 'wikipedia' in self.query:

            setCommandText("Searching...")
            speak('Searching...')
            setWidget("Recognizing")

            self.wikipediaSearch = self.query.replace('wikipedia ', '')
            print(self.wikipediaSearch)
            t1 = threading.Thread(target=image_search(self.wikipediaSearch))
            t1.start()

            try:

                wikipediaSearch = wikipedia.search(self.wikipediaSearch)
                print(wikipediaSearch[0])
                resultSummery = wikipedia.summary(
                    wikipediaSearch[0], sentences=1)
                resultString = f"{wikipediaSearch[0]}\n{resultSummery}"

                # Set Image
                folder_name = self.query.replace(' ', '_')
                image = os.listdir(f'.\\simple_images\\{folder_name}')
                setPixmap(f'.\\simple_images\\{folder_name}\\' + image[0])
                setWidget("Result")
                setCommandText(resultString)
                speak(resultSummery)
                print(resultSummery)
                # Remove Image
                setPixmap("")
                setCommandText('')

            except Exception as e:
                print(e)
                setCommandText("Connection error")
                speak('Connection error')

        else:
            if self.query == 'voice problem':

                # time.sleep(2)
                print("Nothing to search")
                setCommandText('Voice Problem\nSay that again please...')
                speak('Voice Problem\nSay that again please...')
                setWidget('')
            else:
                response = chatBot.chatbot_response(self.query)
                print(response)
                setCommandText(response)
                speak(response)

                print(self.query)
                # print("nothing")
                # speak("nothing")


startListening = MainThread()


class VoiceAssistantUI(QMainWindow):

    def __init__(self):
        super(VoiceAssistantUI, self).__init__()
        self.count = 0
        loadUi(".\\UI\\VoiceAssistant.ui", self)

        self.setWindowIcon(QtGui.QIcon('.\\resources\\logo.png'))
        self.setWindowTitle("Voice Assistant 2.0")

        # Button Function
        self.micButton.clicked.connect(self.startExecution)
        self.micButton.setIcon(QIcon("resources/mic.png"))
        self.exitButton.clicked.connect(self.close)

        # progressBar Update Thread
        self.cpuUsesThreadClass = CpuUsesProgressBar()
        self.cpuUsesThreadClass.start()
        self.cpuUsesThreadClass.get_signal.connect(
            self.updateCpuUsesProgressBar)

        self.ramUsesThreadClass = RamUsesProgressBar()
        self.ramUsesThreadClass.start()
        self.ramUsesThreadClass.get_signal.connect(
            self.updateRamUsesProgressBar)

        self.audioWavesThreadClass = AudioWaves()
        self.audioWavesThreadClass.start()
        self.audioWavesThreadClass.get_signal.connect(self.updateAudioWaves)

        # Set Text to Command Text
        dataSignals.get_text_signal.connect(self.setCommandText)

        # Set Image to imagePixmap
        dataSignals.get_image_signal.connect(self.setPixmapImage)

        # Set Active Widget
        dataSignals.get_active_widget.connect(self.setActiveWidget)

        # self.imagePixmap.setPixmap(QPixmap(".\\UI\\mic.png"))

        self.showWidget = False
        self.audioVisulizationWidget.hide()
        self.processingWidget.hide()
        self.resultWidget.hide()
        self.defaultWidget.show()

        self.movie = QMovie('.\\resources\\processing.gif')
        self.processingLabel.setMovie(self.movie)
        self.movie.start()

        self.getWeather = get_weather('431605')

        self.city_country.setText('{}, {}'.format(
            self.getWeather[0], self.getWeather[1]))
        self.viewIcon.setPixmap(
            QPixmap('.\\weatherInfo\\weatherIcons2\\{}.png'.format(self.getWeather[3])))
        self.temperature.setText('{} °C'.format(self.getWeather[2]))
        self.weather.setText(self.getWeather[4])

        # self.defaultLabel.setText("Hello Sir,\n How Can I help you")
        self.displayTextLabel.setText("Hello Sir,\n How Can I help you")
        # time.sleep(3)
        # speak("Hello Sir,  How Can I help you")

        self.RamDetail.setText(sysInfo.ram_detail())
        self.CPU_Detail.setText(sysInfo.cpu_detail())

        # Refresh time
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)  # Function call
        timer.start(1000)

    def showTime(self):
        dateTimeNow = datetime.datetime.now()

        hour = dateTimeNow.strftime("%I")
        minute = dateTimeNow.strftime("%M")
        second = dateTimeNow.strftime("%S")
        am_pm = dateTimeNow.strftime("%p")

        day = dateTimeNow.strftime("%d")
        month = dateTimeNow.strftime("%m")
        year = dateTimeNow.strftime("%Y")
        dayName = dateTimeNow.strftime("%a")

        self.showTimeLabel.setText(f"{hour}:{minute}:{second}")
        self.showDateLabel.setText(f"{day}-{month}-{year}")
        self.am_pmTextLabel.setText(am_pm)
        self.dayNameLabel.setText(dayName)

    @staticmethod
    def startExecution():
        startListening.start()

    def closeEvent(self, event):
        print("\nExiting...")

    def setCommandText(self, text):
        self.displayTextLabel.setText(str(text))

    def setPixmapImage(self, image):
        setImage = QPixmap(image)
        self.viewLabel.setPixmap(setImage)

    def setActiveWidget(self, text):

        if text == "Listening":
            self.audioVisulizationWidget.show()
            self.processingWidget.hide()
            self.resultWidget.hide()
            self.defaultWidget.hide()

        elif text == "Recognizing":
            self.processingWidget.show()
            self.audioVisulizationWidget.hide()
            self.resultWidget.hide()
            self.defaultWidget.hide()

            self.movie = QMovie('.\\resources\\processing.gif')
            self.processingLabel.setMovie(self.movie)
            self.movie.start()

        elif text == "Result":
            self.resultWidget.show()
            self.audioVisulizationWidget.hide()
            self.processingWidget.hide()
            self.defaultWidget.hide()

        elif text == "Read File":

            try:
                # defaultPath = r'D:\Learning\E-Books'
                defaultPath = r"D:\DYPIMCAM\II_Sem\Mini_Project\Voice Assistant\Voice Assistant 2.0\Testing"

                getFile = QFileDialog.getOpenFileNames(self, 'Select File to Read', defaultPath,
                                                       'Text Files (*.pdf *.doc *.txt)')
                file = getFile[0][0]
                print("Selected File:", file)

                splitFile = os.path.splitext(file)
                fileExtension = splitFile[1]

                if fileExtension == '.pdf':
                    pdfReader = PyPDF2.PdfFileReader(getFile[0][0])
                    page = pdfReader.getPage(1)
                    textRead = page.extractText()
                    speak(textRead)
                elif fileExtension == '.txt':
                    readFile = open(file, 'r')
                    readText = readFile.read()
                    speak(readText)

            except Exception:
                print("File not Selected")
                speak("File not Selected")

        else:
            self.defaultWidget.show()

            self.audioVisulizationWidget.hide()
            self.processingWidget.hide()
            self.resultWidget.hide()

    def updateCpuUsesProgressBar(self, val):
        self.cpu_usesProgressBar.setValue(val)

    def updateRamUsesProgressBar(self, val):
        self.ram_usesProgressBar.setValue(val)

    def updateAudioWaves(self, val):

        self.audioWaveBar5 = val
        self.lineTop1.setGeometry(
            100, 140 - self.audioWaveBar5, 20, 10 + self.audioWaveBar5)
        self.lineBottom1.setGeometry(100, 150, 20, 10 + self.audioWaveBar5)

        self.audioWaveBar2 = val * 2
        self.lineTop2.setGeometry(
            145, 140 - self.audioWaveBar2, 20, 10 + self.audioWaveBar2)
        self.lineBottom2.setGeometry(145, 150, 20, 10 + self.audioWaveBar2)

        self.audioWaveBar3 = val * 3
        self.lineTop3.setGeometry(
            190, 140 - self.audioWaveBar3, 20, 10 + self.audioWaveBar3)
        self.lineBottom3.setGeometry(190, 150, 20, 10 + self.audioWaveBar3)

        self.audioWaveBar4 = val * 2
        self.lineTop4.setGeometry(
            235, 140 - self.audioWaveBar4, 20, 10 + self.audioWaveBar4)
        self.lineBottom4.setGeometry(235, 150, 20, 10 + self.audioWaveBar4)

        self.audioWaveBar5 = val
        self.lineTop5.setGeometry(
            280, 140 - self.audioWaveBar5, 20, 10 + self.audioWaveBar5)
        self.lineBottom5.setGeometry(280, 150, 20, 10 + self.audioWaveBar5)


class CpuUsesProgressBar(QThread):
    get_signal = pyqtSignal(int)

    def __init__(self):
        super(CpuUsesProgressBar, self).__init__()

    def run(self):
        print('Starting thread...')
        while 1:
            val = sysInfo.cpu_uses()
            val = round(val)
            self.get_signal.emit(val)

            # print(val)


class RamUsesProgressBar(QThread):
    get_signal = pyqtSignal(int)

    def __init__(self):
        super(RamUsesProgressBar, self).__init__()

    def run(self):
        print('Starting thread...')
        while 1:
            val = sysInfo.ram_uses()
            val = round(val)
            self.get_signal.emit(val)

            # print(val)


class AudioWaves(QThread):
    get_signal = pyqtSignal(int)

    def __init__(self):
        super(AudioWaves, self).__init__()

    def run(self):
        print('Starting thread...')

        while True:
            try:
                data = np.fromstring(stream.read(1024), dtype=np.int16)
                dataL = data[0::2]
                peakL = np.abs(np.max(dataL) - np.min(dataL)) / maxValue
                lString = 10 * int(peakL * bars)

                self.get_signal.emit(lString)
            except EXCEPTION as e:
                print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = VoiceAssistantUI()
    widget.showFullScreen()
    widget.show()

    sys.exit(app.exec_())
