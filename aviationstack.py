import requests
import json
import pandas as pd

# API Documentation: https://aviationstack.com/documentation
# url for getting real time flights 

key = ""

def get_url(airport, offset=0):
    return f"http://api.aviationstack.com/v1/flights?access_key={key}&dep_iata={airport}&offset={offset}"


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


def data():
  f = open('flights_PIT.json')
  data = json.load(f)

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
  print(df)

if __name__ == "__main__":
    # call_api()
    data()
    

