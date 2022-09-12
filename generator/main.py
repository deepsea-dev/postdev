from time import time
from urllib import request
from aitextgen import aitextgen
from os import environ, makedirs, path
import uuid
import re
import json
import requests

PIXABAY_URL = "https://pixabay.com/api/"

class MissingEnivornmentVariable(Exception): pass

PIXABAY_KEY = environ.get("PIXABAY_KEY")
if (PIXABAY_KEY == None): raise MissingEnivornmentVariable("PIXABAY_KEY is not set")

if (not path.exists("./images/")):
    makedirs("./images/")

# \/\/\/\/ Testing - Please remove afterwards \/\/\/\/
example = {
    "title": "space",
    "tagline": "Space is further than the sky",
    "winner": True,
    "likes": "100",
    "comments": "200",
    "fileID": ""
}

def downloadImage(imageURL):
    print("The image url we got was " + imageURL)
    fileID = str(uuid.uuid4())
    print("The fileID is " + fileID)
    fileName = fileID + ".png"
    print("The fileName is " + fileName)
    imageData = requests.get(imageURL).content
    with open("./images/" + fileName, "wb") as imageFile:
        imageFile.write(imageData)
        imageFile.close()

    return fileName, fileID

SEARCH_PARAMS = {
    "key": PIXABAY_KEY,
    "lang": "en",
    "image_type": "photo",
    "orientation": "horizontal",
    "per_page": 3,
    "safesearch": "true",
}


search_params = {**SEARCH_PARAMS, **{"q": example["title"]}}
response = requests.get(PIXABAY_URL, search_params)
print("Response: " + str(response))
response = response.json()
print("Response (JSON): " + str(response))

if (response["totalHits"] > 0):
    fileName, fileID = downloadImage(response["hits"][0]["previewURL"])

print("Does the api key exist?", PIXABAY_KEY != None)

exit(1)
# /\/\/\/\ Testing - Please remove afterwards /\/\/\/\

ai = aitextgen(model_folder="./", verbose=True)

def mapProject(projectString):
    values = projectString.split(" | ")
    return {
            "title": values[3],
            "tagline": values[4].rstrip(),
            "winner": values[0] == "True",
            "likes": values[1],
            "comments": values[2],
            "fileID": ""
    }

def createBatch(size=100):
    batch = []
    print("Creating batch...")
    while len(batch) < size:
        generated = ai.generate(n = 10, return_as_list=True)
        generated = list(filter(lambda x: re.search(r"(True|False) \| \d+ \| \d+ \| .*? \| .*", x) != None, generated))
        generated = list(map(mapProject, generated))
        batch += generated

        print("{}/{} generated.".format(len(batch), size))

    print("Batch creation finished")
    return batch

content = {
    "time": int(time()),
    "projects": createBatch()
}

def downloadImage(imageURL):
    fileID = str(uuid.uuid4())
    fileName = fileID + ".png"
    imageData = requests.get(imageURL).content
    with open("./images/" + fileName, "wb") as imageFile:
        imageFile.write(imageData)
        imageFile.close()

    return fileName, fileID

SEARCH_PARAMS = {
    "key": PIXABAY_KEY,
    "lang": "en",
    "image_type": "photo",
    "orientation": "horizontal",
    "safesearch": "true",
}

for index, project in enumerate(content["projects"]):
    search_params = {**SEARCH_PARAMS, **{"q": project["title"]}}
    response = requests.get(PIXABAY_URL, search_params).json()
    
    if (response["totalHits"] > 0):
        fileName, fileID = downloadImage(response["hits"][0]["previewURL"])
        content["projects"][index]["fileID"] = fileID

print("Saving projects.json")
with open("./projects.json", "w") as projectsFile:
    json.dump(content, projectsFile)
    projectsFile.close()
print("Saved projects.json")
