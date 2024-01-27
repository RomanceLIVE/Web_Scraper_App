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

# Connecting to the SQLite database
connection = sqlite3.connect("data.db")


# Function to scrape the page source
def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


# Function to extract data from the source
def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


# Function to send email
def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "yourgmail@gmail.com"
    password = "gmailAPIpasskey"

    receiver = "robert.horvath93@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email sent")


# Function to store data in the database
def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("Insert into events values(?,?,?)", row)
    connection.commit()


# Function to read data from the database
def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    Band, City, Date = row
    cursor = connection.cursor()
    cursor.execute("Select * from events where Band=? and City=? and Date=?", (Band, City, Date))
    rows = cursor.fetchall()
    print(rows)
    return rows

# Main program execution
if __name__ == "__main__":
    # Continuously scrape and process data
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                # Store only if event is new
                store(extracted)
                send_email(message="New event !")
        time.sleep(2)
