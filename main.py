from aviationstack import get_airport_flights, to_df, df_from_file
import airportsdata
from lounges import get_lounges
from weatherAPI import get_forecast
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def main():

  airports = airportsdata.load(code_type="iata")

  print("Welcome to LoungeEasy! Use previous data? (PIT -> DFW on 2/24)? Enter y or yes")

  usePrevData = input().strip()

  if usePrevData == 'y' or usePrevData == 'yes':
    departure_df = df_from_file('sample_PIT_2023-02-24.json')
    departure_iata = "PIT"
    departure_airport = airports[departure_iata]
    destination_df = df_from_file('sample_DFW_2023-02-24.json')
    destination_iata = "DFW"
    destination_airport = airports[destination_iata]

  else:
    print("Type in the IATA code of your origin airport (ie PIT for the Pittsburgh International Airport")
    departure_iata = input()

    try:
      departure_airport = airports[departure_iata]
    except:
      print(f"Sorry! Airport {departure_iata} not found. Exiting")
      return

    departure_data = get_airport_flights(departure_iata)
    departure_df = to_df(departure_data)

    print("Type in the IATA code of your destination airport (ie PIT for the Pittsburgh International Airport")
    destination_iata = input()

    try:
      destination_airport = airports[destination_iata]
    except:
      print(f"Sorry! Airport {departure_iata} not found. Exiting")
      return

    destination_data = get_airport_flights(destination_iata)
    destination_df = to_df(destination_data)


  # Data analysis and visualziation after setting departure/destination airports

  departure_lounges = get_lounges(departure_iata)

  print(f"Lounges from {departure_airport['iata']}: {departure_lounges}")

  dest_forecast = get_forecast(lat=destination_airport["lat"], lon=destination_airport["lon"])
  dep_forecast = get_forecast(lat=departure_airport["lat"], lon=departure_airport["lon"])


  n = len(dest_forecast['list'])

  dest_forecast_df = {
    f'{destination_airport["city"]}': [dest_forecast['list'][i]['main']['temp'] for i in range(n)],
    f'{departure_airport["city"]}': [dep_forecast['list'][i]['main']['temp'] for i in range(n)],
    #'feels_like': [dest_forecast['list'][i]['main']['feels_like'] for i in range(n)],
    'dt': [datetime.fromtimestamp(dest_forecast['list'][i]['dt']).strftime("%m/%d, %H:%M") for i in range(n)]
  }

  df = pd.DataFrame.from_dict(dest_forecast_df).set_index('dt')


  df.plot.line(linewidth=.75)
  plt.xticks(ticks = range(0,len(df.index), 3),labels = df.index[::3], rotation = 30)
  plt.gcf().subplots_adjust(bottom=.3)
  plt.ylabel("Temperature (F)")
  plt.xlabel("Date and Time")


  plt.show()



main()