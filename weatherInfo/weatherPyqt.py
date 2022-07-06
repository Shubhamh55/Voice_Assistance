import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import datetime
from threading import Timer
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import requests
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')
weatherAPI_key = config['weather_api']['weather_key']

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'


def get_weather(city):
    result = requests.get(url.format(city, weatherAPI_key))
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


class CheckingUI(QMainWindow):
    def __init__(self):
        super(CheckingUI, self).__init__()
        loadUi("weatherUI.ui", self)


        self.searchButton.clicked.connect(self.search)

        self.searchCity = self.search_city.setText("hadgaon")

        self.searchCity = self.search_city.text()
        self.getWeather = get_weather(self.searchCity)

        self.city_country.setText('{}, {}'.format(self.getWeather[0], self.getWeather[1]))
        self.viewIcon.setPixmap(QPixmap('.\\weatherIcons2\\{}.png'.format(self.getWeather[3])))
        self.temperature.setText('{} °C'.format(self.getWeather[2]))
        self.weather.setText(self.getWeather[4])

    def search(self):

        try:
            self.searchCity = self.search_city.text()
            self.getWeather = get_weather(self.searchCity)

            self.city_country.setText('{}, {}'.format(self.getWeather[0], self.getWeather[1]))
            self.viewIcon.setPixmap(QPixmap('.\\weatherIcons2\\{}.png'.format(self.getWeather[3])))
            self.temperature.setText('{} °C'.format(self.getWeather[2]))
            self.weather.setText(self.getWeather[4])
            print(self.getWeather[3])
        except Exception as e:
            massageBox = QMessageBox()
            massageBox.setWindowTitle('Error')
            massageBox.setText(str(e))
            massageBox.setIcon(QMessageBox.Critical)
            massageBox.exec_()
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CheckingUI()

    widget.setGeometry(160, 90, 800, 450)
    widget.show()


    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
