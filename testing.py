import requests
from bs4 import BeautifulSoup

URL = "https://www.eventbrite.com/b/online/holiday/fall-events/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def scrape_event_titles(url, headers=HEADERS):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Update this line to match the appropriate HTML element and class for event titles
    event_titles = soup.find_all("YOUR_HTML_ELEMENT", class_="YOUR_CLASS_NAME")

    for title in event_titles:
        print(title.text.strip())


if __name__ == "__main__":
    scrape_event_titles(URL)
