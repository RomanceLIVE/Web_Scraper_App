import requests
import selectorlib
import smtplib, ssl
import os

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    # Scrape the page source
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "robert.horvath93@gmail.com"
    password = "mpxfsbxuxubqztxp"

    receiver = "robert.horvath93@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email sent")


def store(extracted):
    if extracted and extracted != "No upcoming tours":
        # Check for duplicates
        with open("data.txt", "r") as file:
            existing_data = file.read().splitlines()
        if extracted not in existing_data:
            with open("data.txt", "a") as file:  # a for append
                file.write(extracted + "\n")


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)  # only store when event new
            send_email(message="New event !")
