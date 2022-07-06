from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
weatherAPI_key = config['weather_api']['weather_key']
newsAPI_key = config['news_api']['news_key']

print(weatherAPI_key)
print(newsAPI_key)
