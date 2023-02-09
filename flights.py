from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv
import airportsdata

s = HTMLSession()


def get_url(airline, offset):
    return f"https://flightaware.com/live/fleet/{airline}?;offset={offset};order=ident;sort=ASC"


def get_page(airline, offset):
    def do():
        url = get_url(airline, offset)
        response = s.get(url)
        response.html.render()
        soup = BeautifulSoup(response.html.html, "lxml")
        curRow = None
        data = []
        for elem in soup.find_all("td", attrs={"class": ["smallrow1", "smallrow2"]}):
            if elem['class'] != curRow:
                curRow = elem['class']
                data.append([])
            data[-1].append(elem.text.strip())

        return data

    try:
        return do()
    except:
        # retry once
        try:
            return do()
        except:
            print(
                f"Failed after second attempt for airline {airline} on page {offset // 20}")
            return []


def scrape():
    print('Enter an airline code (ie AAL for American Airlines):')
    airline = input()

    data = []
    L = [None]
    i = 0
    while len(L) != 0:
        L = get_page(airline, i*20)
        if L:
            print(f"Scraped page {i}")
        i += 1
        data.extend(L)

    # name of csv file
    filename = f"{airline}-flights-raw.csv"

    fields = ["Flight Number", "Type", "Origin", "Destination",
              "Departure Time", "Estimated Arrival Time"]

    # writing to csv file
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)


def clean():

    def cleanAirport(airport):
        cleaned = airport.replace(')', '').split('(')[-1].strip()
        if '/' in cleaned:
            cleaned = cleaned.split('/')[1].strip()
        cleaned = airports[cleaned]['iata']
        return cleaned

    print('Enter an airline code (ie AAL for American Airlines) with data to clean:')
    airline = input()
    
    # name of csv files
    input_filename = f"{airline}-flights-raw.csv"
    output_filename = f"{airline}-flights-clean.csv"

    airports = airportsdata.load()

    with open(output_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile) 
        with open(input_filename, mode='r') as file:
            csvFile = csv.reader(file)

            first = True

            for line in csvFile:
                # remove airplane type column
                line = [line[0]] + line[2:]
                # write header
                if first:
                    first = False
                    csvwriter.writerow(line) 
                # write data lines
                else:
                    # remove airline code from flight number
                    line[0] = line[0].replace(airline, '')
                    # convert airport info to just IATA codes
                    line[1] = cleanAirport(line[1])
                    line[2] = cleanAirport(line[2])

                    csvwriter.writerow(line) 


if __name__ == "__main__":
    scrape()
    clean()
