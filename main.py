from aviationstack import get_airport_flights, to_df, df_from_file, plotDelay, get_flight_info
import airportsdata
from lounges import get_lounges
from weatherAPI import get_forecast
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def main():
    # load airport data from python module, with iata codes
    airports = airportsdata.load(code_type="iata")

    # prompt to use previous data
    print("Welcome to LoungeEasy! With information about your departure and arrival airport, we can provide information such as weather, lounges, and global flight information.")
    print("Use previous data? Enter y or yes")

    usePrevData = input().strip()

    # user chooses previous data to use
    if usePrevData == 'y' or usePrevData == 'yes':
        print("Choose from the following options:")
        print("Enter '1' for PIT -> DFW on 2/24")
        print("Enter '2' for PIT -> MDW on 3/1")
        print("Enter '3' for DAL -> BNA on 3/2")
        i = input()
        if i == '1':
            departure_df = df_from_file('sample_PIT_2023-02-24.json')
            departure_iata = "PIT"
            departure_airport = airports[departure_iata]
            destination_df = df_from_file('sample_DFW_2023-02-24.json')
            destination_iata = "DFW"
            destination_airport = airports[destination_iata]
        elif i == '2':
            departure_df = df_from_file('sample_PIT_2023-03-01.json')
            departure_iata = "PIT"
            departure_airport = airports[departure_iata]
            destination_df = df_from_file('sample_MDW_2023-03-01.json')
            destination_iata = "MDW"
            destination_airport = airports[destination_iata]
        elif i == '3':
            departure_df = df_from_file('sample_DAL_2023-03-02.json')
            departure_iata = "DAL"
            departure_airport = airports[departure_iata]
            destination_df = df_from_file('sample_BNA_2023-03-02.json')
            destination_iata = "BNA"
            destination_airport = airports[destination_iata]
        else:
            print("Invalid option. Exiting.")
            return

    else:
        # Calls API from aviationstack.py file to get real time data
        print("Querying real-time flight information. Note that the current API usage is limited to 100 requests / month. If you run into issues querying data, please sign up for a new API key at https://aviationstack.com/.")
        print(
            "Type in the IATA code of your origin airport (ie PIT for the Pittsburgh International Airport)")
        departure_iata = input()

        try:
            departure_airport = airports[departure_iata]
        except:
            print(f"Sorry! Airport {departure_iata} not found. Exiting")
            return

        print(f"Getting flight information for {departure_iata}...\n")
        departure_data = get_airport_flights(departure_iata)

        departure_df = to_df(departure_data)

        print(
            "Type in the IATA code of your destination airport (ie PIT for the Pittsburgh International Airport)")
        destination_iata = input()

        try:
            destination_airport = airports[destination_iata]
        except:
            print(f"Sorry! Airport {departure_iata} not found. Exiting")
            return

        print(f"Getting flight information for {destination_iata}...\n")
        destination_data = get_airport_flights(destination_iata)
        destination_df = to_df(destination_data)

    # infinite loop to simulate menu
    while True:
        print("Enter a command (not case-sensitive). For example to get lounges, enter 'L' or 'Lounges'. To see all commands, enter 'H' or 'Help'. Enter 'Q' or 'Quit' to exit.")

        command = input()
        command = command.lower()

        # Quit / exit command
        if command == 'q' or command == 'quit':
            return

        # Help command
        elif command == 'h' or command == 'help':
            print("""
Flight delay visualizations: 'D' or 'delay'
Weather: 'W' or 'Weather'
Lounges: 'L' or 'Lounge'
Quit: 'Q' or 'Quit'
Specific flight information: 'F' or 'Flight'
      """)

        # weather command, creates line graph and message about temperature
        elif command == 'w' or command == 'weather':
            print("Getting weather information...")

            # gets forecast for both airports based on lat/long location
            dep_forecast = get_forecast(
                lat=departure_airport["lat"], lon=departure_airport["lon"])

            dest_forecast = get_forecast(
                lat=destination_airport["lat"], lon=destination_airport["lon"])

            # uses numpy to store temperature time series data
            n = len(dest_forecast['list'])
            forecast_temp = np.zeros((n, 2))
            for i in range(n):
                forecast_temp[i][0] = dest_forecast['list'][i]['main']['temp']
                forecast_temp[i][1] = dep_forecast['list'][i]['main']['temp']

            # uses numpy for statistical analysis
            dest_avg_tmp = np.average(forecast_temp[:, 0])
            dep_avg_tmp = np.average(forecast_temp[:, 1])
            std_dev = np.std(forecast_temp)

            # message prompts based on temperature differences. Uses standard deviation to determine how different temperature will be
            if dest_avg_tmp > dep_avg_tmp:
                if (std_dev > 12):
                    print("Woah! It's a lot warmer where you're going!")
                if (std_dev < 7):
                    print("The temperature won't change much where you're going!")
                print(
                    f"It will be about {int(dest_avg_tmp - dep_avg_tmp)} degrees warmer in {destination_airport['city']}.\n")
            else:
                if (std_dev > 10):
                    print("Woah! It's a lot colder where you're going!")
                if (std_dev < 7):
                    print("The temperature won't change much where you're going!")
                print(
                    f"It will be about {int(dep_avg_tmp - dest_avg_tmp)} degrees colder in {destination_airport['city']}.\n")

            # convert to a pandas df
            dt_list = [datetime.fromtimestamp(dest_forecast['list'][i]['dt']).strftime(
                "%m/%d, %H:%M") for i in range(n)]
            df = pd.DataFrame(data=forecast_temp, index=dt_list,
                              columns=[destination_airport['city'], departure_airport['city']])

            # Create and display line plot
            df.plot.line(linewidth=.75)
            plt.xticks(ticks=range(0, len(df.index), 3),
                       labels=df.index[::3], rotation=30)
            plt.gcf().subplots_adjust(bottom=.3)
            plt.ylabel("Temperature (F)")
            plt.xlabel("Date and Time")
            plt.show()

        # command to get lounges
        elif command == 'l' or command == 'lounges':
            print("Departure airport (d) or Arrival airport (a)?")
            airport = input()
            airport = airport.lower()
            if airport == 'd':
                iata = departure_iata

            elif airport == 'a':
                iata = destination_iata
            else:
                print("Invalid option.")

            print("Getting lounge information...\n")

            # gets lounges and creates readable string
            airport, lounges = get_lounges(iata)
            if airport == None or lounges == None:
                print(f"No lounges found in {iata}.\n")
            else:
                lounges_str = ""
                for terminal in lounges:
                    lounges_str += f"{terminal}: {', '.join(lounges[terminal])}\n"

                print(f"Lounges from {airport}:\n{lounges_str}")

        # visualizes flight delay info
        elif command == 'd' or command == 'delay':

            print("Departure airport (d) or Arrival airport (a)?")
            airport = input()
            airport = airport.lower()
            if airport == 'd':
                plotDelay(departure_df, "departure", departure_iata)
            elif airport == 'a':
                plotDelay(destination_df, "arrival", destination_iata)
            else:
                print("Invalid option.")

        # queries flight data to get specific flight information
        elif command == 'f' or command == 'flight':
            print(
                "Enter your IATA Flight number (ie 'AA892') for American Airlines flight 892.")
            flight_num = input().upper()
            info = get_flight_info(destination_df, departure_df, flight_num)
            if info is None:
                print(f"Sorry, I could not find flight {flight_num}.")
            else:
                print(info)

        else:
            print("Invalid command. Enter 'h' or 'help' for options.")


if __name__ == "__main__":
    main()
