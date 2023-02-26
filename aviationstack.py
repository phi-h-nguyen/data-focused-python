import requests
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


# API Documentation: https://aviationstack.com/documentation
# url for getting real time flights 

key = "80d5a096bf3bf3af36fcf446192ffbe6"

def get_url(airport, offset=0):
    return f"http://api.aviationstack.com/v1/flights?access_key={key}&dep_iata={airport}&offset={offset}"


def get_airport_flights(airport):
    url = get_url(airport)
    response = requests.get(url)
    json_obj = response.json()
    print(response)
    print(json_obj)
    # print(response.content)

    data = json_obj['data']

    total = json_obj['pagination']['total']
    for i in range(1, min(total // 100, 9) + 1):
      url = get_url(airport)
      response = requests.get(url, i * 100)
      json_obj = response.json()
      data.extend(json_obj['data'])


    now = datetime.now()

    with open(f"flights_{airport}_{str(now)}.json", "w") as outfile:
      json.dump(data, outfile)

    return data


def call_api():
    print('Enter an IATA airport code (ie PIT for Pittsburgh International Airport). Will query a maximum of 1000 flights.:')
    airport = input()
    url = get_url(airport)

    response = requests.get(url)
    json_obj = response.json()
    print(response)
    print(json_obj)
    # print(response.content)

    data = json_obj['data']

    total = json_obj['pagination']['total']
    for i in range(1, min(total // 100, 9) + 1):
      url = get_url(airport)
      response = requests.get(url, i * 100)
      json_obj = response.json()
      print(f"Flight # {i * 100}: {json_obj['data'][0]}")
      data.extend(json_obj['data'])

    with open(f"flights_{airport}.json", "w") as outfile:
      json.dump(data, outfile)


def to_df(data):
  df_dict = {
    'flight_date': [],
    'flight_status': [],
    'departure-airport': [],
    'departure-timezone': [],
    'departure-iata': [],
    'departure-scheduled': [],
    'departure-estimated': [],
    'departure-actual': [],
    'departure-delay': [],
    'departure-terminal': [],
    'departure-gate': [],
    'arrival-airport': [],
    'arrival-timezone': [],
    'arrival-iata': [],
    'arrival-scheduled': [],
    'arrival-estimated': [],
    'arrival-actual': [],
    'arrival-delay': [],
    'arrival-terminal': [],
    'arrival-gate': [],
    'airline-name': [],
    'airline-iata': [],
    'flight-number': [],
    'flight-iata': [],
    'flight-icao': [],
  }

  for i in range(len(data)):
    flight_info = data[i]
    for key in df_dict.keys():
      index = key.split('-')
      if len(index) == 1:
        df_dict[key].append(flight_info[index[0]])
      if len(index) == 2:
        df_dict[key].append(flight_info[index[0]][index[1]])

  df = pd.DataFrame.from_dict(df_dict).set_index('flight-icao')
  return df

def plotDelay(df):
    # Group the data by airline and calculate the total delay
    airline_delays = df.groupby('airline-name')['departure-delay'].sum()

    # Get the top 10 airlines with the most delay
    top_airlines = airline_delays.nlargest(10)

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(top_airlines.values, labels=top_airlines.index, autopct='%1.1f%%')
    plt.title('Top 10 Airlines with the Most Delay')
    plt.show()


    grouped_df = df.groupby(['airline-name'])


    fig, ax1 = plt.subplots(figsize=(15, 7))
    for name, group in grouped_df:
        delays = group['departure-delay'].fillna(0)
        ax1.hist(delays, bins=range(0, 24, 1), alpha=0.5, label=name)
        counts, bin_edges = np.histogram(delays, bins=range(0, 24, 1))

        labels = []
        for i in range(len(counts)):
            labels.append('{}-{} min: {}'.format(int(bin_edges[i]), int(bin_edges[i + 1]), counts[i]))
        # for i, v in enumerate(ax1.hist(delays, bins=range(0, 24, 1), alpha=0.5, label=name)[0]):
        #     ax1.text(i, v + 1, str(int(v)))

    # Set the x-axis and y-axis labels and title
    ax1.set_xlabel('Delay (hours)')
    ax1.set_ylabel('Number of Flights')
    ax1.set_title('Flight Delays by Airline')
    # Add a legend
    # ax1.legend(loc='upper left', bbox_to_anchor=(0.9, 1))
    ax1.legend(labels=labels)
    plt.subplots_adjust(right=0.9)
    # Show the plot
    plt.show()
    delays = df['departure-delay'].fillna(0)

    plt.hist(delays, bins=range(0, 24, 1), color='red')
    plt.xlabel('Delays(hours)')
    plt.ylabel('Number of Flights')
    for i, v in enumerate(plt.hist(delays, bins=range(0, 24, 1), color='red')[0]):
        plt.text(i, v + 1, str(int(v)))

    plt.show()

def df_from_file(file = 'flights_PIT.json'):
  f = open(file)
  data = json.load(f)
  return to_df(data)

if __name__ == "__main__":
    # call_api()
    df = df_from_file()
    plotDelay(df)


