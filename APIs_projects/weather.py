import json
import requests
import time



def get_humanDate(epochime):
    human_read_date = time.strftime("%d-%m-%Y", time.gmtime(epochime))
    return human_read_date

def get_humanTime(epochtime):
    human_read_time = time.strftime("%d-%m-%Y %H:%M", time.gmtime(epochtime))
    return human_read_time

def general_informations(json_response):
    infos = []

    #position
    latitude = json_response['lat']
    longitude = json_response['lon']
    timezone = json_response['timezone']
    position = f"Your postion's latitude: {latitude}\nYour position's longitude: {longitude}\nYour position's timezone: {timezone}"
    infos.append(position)
    return infos

def current_weather(json_response):
    infos = []
    current = json_response['current']

    #weather's condition informations 
    current_weather = current['weather'][0]
    current_description = f"Weather's quick description: {current_weather['description']}"
    infos.append(current_description)

    #temperature(feels like)
    feels_like = f"Temperature: {current['feels_like']}°C"
    infos.append(feels_like)

    #humidity in percentage
    humidity = f"Humidity: {current['humidity']}%"
    infos.append(humidity)

    #cloudiness in percentage
    cloudiness = f"Cloud conditions: {current['clouds']}%"
    infos.append(cloudiness)
    return infos

def hourly_weather(json_response):
    infos = []
    hour = json_response['hourly'][0]

    #weather's conditions information
    weather = hour['weather'][0]
    description = f"Weather's quick description: {weather['description']}"
    infos.append(description)

    #temperature(feels like)
    temperature = f"Temperature: {hour['feels_like']}°C"
    infos.append(temperature)

    #humidity in percentage
    humidity = f"Humidity: {hour['humidity']}%"
    infos.append(humidity)

    #clodiness in percantage
    cloudiness = f"Cloud conditions: {hour['clouds']}%"
    infos.append(cloudiness)
    return infos

def daily_weather(json_response):
    infos = []
    day = json_response['daily'][0]

    #date of weather requests
    epoch = day['dt']
    converted_date = get_humanDate(epoch)
    date = f"Date: {converted_date}"
    infos.append(date)
    
    #weather's conditions information
    weather = day['weather'][0]
    description = f"Weather's quick description: {weather['description']}"
    infos.append(description)

    #temperature(feels like)
    temperature = f"Temperature: {day['feels_like']['day']}°C"
    infos.append(temperature)

    #morning temperature(feels like)
    morning_temperature = f"Morning temperature: {day['feels_like']['morn']}°C"
    infos.append(morning_temperature)

    #night temperature(feels like)
    night_temperature = f"Night temperature: {day['feels_like']['night']}°C"
    infos.append(night_temperature)

    #max temperature
    max_temperature = f"Max temperature of the day: {day['temp']['max']}°C"
    infos.append(max_temperature)

    #min temperature
    min_temperature = f"Min temperature of the day: {day['temp']['min']}°C"
    infos.append(min_temperature)

    #humidity
    humidity = f"Humidity: {day['humidity']}%"
    infos.append(humidity)

    #cloudiness
    cloudiness = f"CloudinessL {day['clouds']}%"
    infos.append(cloudiness)

    #sunrise
    epoch_sunrise = day['sunrise']
    converted_sunrise = get_humanTime(epoch_sunrise)
    sunrise = f"Sunrise: {converted_sunrise}"
    infos.append(sunrise)

    #sunset
    epoch_sunset = day['sunset']
    converted_sunset = get_humanTime(epoch_sunset)
    sunset = f"Sunset: {converted_sunset}"
    infos.append(sunset)
    return infos


latitude = str(input("Insert the latitude of the position: "))
longitude = str(input("Insert the longitude of the position: "))
key = str(input("Insert your generated key on https://home.openweathermap.org/: "))

try:
    endpoint = f"https://api.openweathermap.org/data/2.5/onecall?&lat={latitude}&lon={longitude}&lan=it&units=metric&exclude=alert&appid={key}"
    response = requests.get(endpoint)
    response_status_code = response.status_code

    if response_status_code == 200:
        json_response = response.json()

        weather_information = str(input("current, hourly, or daily: "))

        if weather_information == "current":
            for c in current_weather(json_response):
                print(c)
        elif weather_information == "hourly":
            for h in hourly_weather(json_response):
                print(h)
        elif weather_information == "daily":
            for d in daily_weather(json_response):
                print(d)
        else:
            print("SOMETHING WENT WRONG WITH YOUR INPUT, CHANGE IT!")

    else:
        print("SOMETHING WENT WRONG WITH THE REQUEST!")
        
except:
    print("SOMETHING WRONG WITH YOUR INPUTS!")