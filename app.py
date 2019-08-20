from flask import Flask
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/person")
def get_person():
    headers = {
        "referer": "https://www.google.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    }

    r = requests.get("https://www.fakenamegenerator.com/", headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Name and address
    name = soup.find("div", {"class": "address"}).find("h3").text.strip()
    address = soup.find("div", {"class": "adr"}).text.strip()
    print(name, address)

    info = {"name": name, "address": address}

    # Extra details
    extraContent = soup.find("div", {"class": "extra"})
    extraContentList = extraContent.find_all("dl")

    for i, dl in enumerate(extraContentList):
        key = dl.find("dt").text
        value = dl.find("dd").text
        if key == "SSN":
            value = value[0:11]

        if key == "Email Address":
            value = re.split(" ", value)[0]

        if key != "QR Code":
            info[key] = value

    return info


if __name__ == '__main__':
    app.run()
