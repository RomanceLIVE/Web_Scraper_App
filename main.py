import requests
import selectorlib


URL = "http://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    # Scrape the page source
    response = requests.get(URL)
    source = response.text
    return source


if __name__ == "__main__":
    print(scrape(URL))

