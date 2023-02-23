import requests
import json
import csv
import os

rawDataCSV =  open("weatherraw.csv", "w", newline='', encoding='utf-8')
cleanDataCSV =  open("weatherclean.csv", "w", newline='', encoding='utf-8')
writerRaw = csv.writer(rawDataCSV)
writerClean = csv.writer(cleanDataCSV)
     
writerRaw.writerow(["City", "API Output"])
writerClean.writerow(["City","Temperature (in kelvin unit)","Pressure","Humidity","Description"])

def weather_forecast(city):
    api_key = os.environ['API_KEY']
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
        # print("Temperature (in kelvin unit) = " +
        #             str(current_temperature) +
        #   "\nPressure = " +
        #             str(current_pressure) +
        #   "\nHumidity = " +
        #             str(current_humidity) +
        #   "\nDescription = " +
        #             str(weather_description))
    else:
        print("City Not Found")
    
cities=["Pittsburgh","New York","London","New Delhi","Paris","Oslo","Bern","Tokyo","Sydney","Los Angeles"]
# city = input("Enter city name: ")
for city in cities:
    # print("Today's Weather:")
    weather_forecast(city)