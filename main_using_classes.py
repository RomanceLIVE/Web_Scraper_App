import smtplib
import sqlite3
import ssl
import time
import requests
import selectorlib

# Constants to access data from the url
URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    # Function to scrape the page source
    def scrape(self, url):
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    # Function to extract data from the source
    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    # Function to send email
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "yourgmail@gmail.com"
        password = "gmailAPIpasskey"

        receiver = "yourgmail@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)
        print("Email sent")


class Database:

    def __init__(self, database_path):
        # Connecting to the SQLite database
        self.connection = sqlite3.connect(database_path)
    # Function to store data in the database
    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("Insert into events values(?,?,?)", row)
        self.connection.commit()

    # Function to read data from the database
    def read(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        Band, City, Date = row
        cursor = self.connection.cursor()
        cursor.execute("Select * from events where Band=? and City=? and Date=?", (Band, City, Date))
        rows = cursor.fetchall()
        print(rows)
        return rows


# Main program execution
if __name__ == "__main__":
    # Continuously scrape and process data
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            data = Database(database_path="data.db")
            row = data.read(extracted)
            if not row:
                # Store only if event is new
                data.store(extracted)
                email = Email()
                email.send(message="New event !")
        time.sleep(2)
