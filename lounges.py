from bs4 import BeautifulSoup
from requests_html import HTMLSession

s = HTMLSession()

def get_url(code):
  return f"https://next.loungebuddy.com/en/{code}?currency=USD"


def get_lounges(code):
  
  url = get_url(code)
  response = s.get(url)
  response.html.render()

  soup = BeautifulSoup(response.html.html, "lxml")

  terminals = {}
  curTerminal = None

  airport_name = soup.find("p", attrs={"class": ["text-sm text-espresso-light"]}).text

  for elem in soup.find_all(attrs={"class": ["title-2", "title-3"]}):
    if elem.text == "Quick Filter":
      continue
    if elem.name == "h3":
      terminals[elem.text] = []
      curTerminal = elem.text
    else:
      terminals[curTerminal].append(elem.text)

  return airport_name, terminals

def main():
  # airports = ["DFW", "SFO", "LGA", "DEN", "ATL", "ORD", "LAX", "CLT", "MCO", "XXX"]

  print('Enter a list of comma separated airport codes (ie "DFW, LAX, CLT"):')
  airports = input()
  airports = [elem.strip() for elem in airports.split(",")]

  for code in airports:
    try:
      airport_name, dict = get_lounges(code)
      print(f"\n{code} ({airport_name}): ")
      for terminal, lounges in dict.items():
        print(f"{terminal}: {', '.join(lounges)}")
    except:
      print(f"\nNo lounges found for airport {code}.")

if __name__ == "__main__":
    main()
