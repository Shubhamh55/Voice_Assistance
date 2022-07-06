from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
import requests


config = ConfigParser()
config.read('config.ini')
weatherAPI_key = config['weather_api']['weather_key']

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'




def search():
    city = city_entry.get()
    weather = get_weather(city)

    try:
        location_label['text'] = '{}, {}'.format(weather[0], weather[1])
        image['bitmap'] = '.\\weatherIcons\\{}.png'.format(weather[3])
        temperature_label['text'] = '{:.2f}°C'.format(weather[2])
        weather_label['text'] = weather[4]
    except Exception as e:
        messagebox.showerror("Error", e)


print(get_weather("hadgaon"))

app = Tk()
app.title("Weather  App")
app.geometry('400x225')

city_name = StringVar()
city_entry = Entry(app, textvariable=city_name)
city_entry.pack()

search_btn = Button(app, text="search", width=12, command=search)
search_btn.pack()

location_label = Label(app, text="Location", font=('bold', 20))
location_label.pack()

image = Label(app, bitmap='')
image.pack()

temperature_label = Label(app, text='temperature')
temperature_label.pack()

weather_label = Label(app, text='Weather')
weather_label.pack()


app.mainloop()
