from fileinput import filename
from time import time
from aitextgen import aitextgen
from google_images_search import GoogleImagesSearch
from os import environ
from os.path import isfile
import random
import uuid
import re
import json

class MissingEnivornmentVariable(Exception): pass

IMAGES_API_KEY = environ.get("IMAGES_API_KEY")
IMAGES_CX = environ.get("IMAGES_CX")
if (IMAGES_API_KEY == None): raise MissingEnivornmentVariable("IMAGES_API_KEY is not set")
if (IMAGES_CX == None): raise MissingEnivornmentVariable("IMAGES_CX is not set")

ai = aitextgen(model_folder="./", verbose=True)

def mapProject(projectString):
    values = projectString.split(" | ")
    return {
            "title": values[3],
            "tagline": values[4].rstrip(),
            "winner": values[0] == "True",
            "likes": values[1],
            "comments": values[2]
    }

def createBatch(size=5):
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

SEARCH_PARAMS = {
    "num": 1,
    "fileType": "png",
    "safe": "high"
}
with GoogleImagesSearch(IMAGES_API_KEY, IMAGES_CX) as imageSearch:
    for index, project in enumerate(content["projects"]):
        search_params = {**SEARCH_PARAMS, **{"q": project["title"], "imgType": random.choice(["clipart", "stock"])}}
        id = str(uuid.uuid4())
        fileName = "{}.png".format(id)
        imageSearch.search(search_params, path_to_dir="./images/", custom_image_name=fileName, width=600, height=400)
        if (isfile("./images/" + fileName)): content["project"][index]["id"] = id

print("Saving projects.json")
with open("./projects.json", "w") as projectsFile:
    json.dump(content, projectsFile)
    projectsFile.close()
print("Saved projects.json")
