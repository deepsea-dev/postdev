from bs4 import BeautifulSoup
import requests
import json


DEVPOST_URL = "https://devpost.com/software/popular?page={}"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
entries = []
while len(entries) < 5000:
    url = DEVPOST_URL.format(len(entries) // 24 + 1)
    print("Fetching {}. Number of entries collected: {}"
        .format(url, len(entries)))
    page = requests.get(
        DEVPOST_URL.format(len(entries) // 24 + 1),
        headers=headers
    )
    soup = BeautifulSoup(page.text, "html.parser")
    projects = soup.find_all("div", {"class": "gallery-entry"})

    projects = [
        {
            "title": project.figure.figcaption.div.h5.text.strip(),
            "tagline": project.figure.figcaption.div.p.text.strip()
        }

        for project in projects
    ]
    entries += projects

    with open("entries.json", "w") as entriesFile:
        json.dump(entries, entriesFile)