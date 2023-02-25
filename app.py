from aviationstack import get_airport_flights, to_df, df_from_file
import airportsdata
from lounges import get_lounges
from weatherAPI import get_forecast


def main():

  airports = airportsdata.load(code_type="iata")

  print("Welcome to LoungeEasy! Use previous data? (PIT -> DFW on 2/24)? Enter y or yes")

  usePrevData = input().strip()

  if usePrevData == 'y' or usePrevData == 'yes':
    #departure_df = df_from_file('flights_PIT_2023-02-24 14:17:21.097057.json')
    departure_iata = "PIT"
    departure_airport = airports[departure_iata]
    #destination_df = df_from_file('flights_DFW_2023-02-24 14:21:55.421591.json')
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

  departure_lounges = get_lounges(departure_iata)
  print(departure_lounges)

  print(destination_airport["city"])
  print(get_forecast(destination_airport["city"]))




main()