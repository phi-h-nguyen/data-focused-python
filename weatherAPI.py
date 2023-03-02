import requests
import csv
import os

rawDataCSV =  open("weatherraw.csv", "w", newline='', encoding='utf-8')
cleanDataCSV =  open("weatherclean.csv", "w", newline='', encoding='utf-8')
writerRaw = csv.writer(rawDataCSV)
writerClean = csv.writer(cleanDataCSV)
     
writerRaw.writerow(["City", "API Output"])
writerClean.writerow(["City","Temperature (in kelvin unit)","Pressure","Humidity","Description"])

def weather_forecast(city):
    api_key = '0a80a58f1e33f376cb5d7cacf503443a'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city

    response = requests.get(complete_url)
    x = response.json()
    # print(city)
    if x["cod"] != "404":
        # print(x)
        writerRaw.writerow([city,x])
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        writerClean.writerow([city, str(current_temperature), str(current_pressure), str(current_humidity), str(weather_description)])

    else:
        print("City Not Found")

# gets forecast given a long and lat
def get_forecast(*, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&limit=1&appid=0a80a58f1e33f376cb5d7cacf503443a&units=imperial"
    response = requests.get(url)
    return response.json()