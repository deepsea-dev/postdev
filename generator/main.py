from aitextgen import aitextgen
import re
import json

ai = aitextgen(model_folder="./")

def mapProject(projectString):
    values = projectString.split(" | ")
    return {
            "title": values[3],
            "tagline": values[4].rstrip(),
            "winner": values[0] == "True",
            "likes": values[1],
            "comments": values[2]
    }

def createBatch(size=100):
    batch = []
    while len(batch) < size:
        generated = ai.generate(n = 10, return_as_list=True)
        generated = list(filter(lambda x: re.search(r"(True|False) \| \d+ \| \d+ \| .*? \| .*", x) != None, generated))
        generated = list(map(mapProject, generated))
        batch += generated
    
    return batch

batch = createBatch()
with open("./projects.json", "w") as batchFile:
    json.dump(batch, batchFile)
    batchFile.close()