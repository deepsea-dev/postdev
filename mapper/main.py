import json

with open('../entries.json', "r") as entriesJSONFile:
    entries = json.load(entriesJSONFile)

    entries = ["{} | {} | {} | {} | {}\n".format(
        entry["winner"],
        entry["likes"],
        entry["comments"],
        entry["title"],
        entry["tagline"]
    ) for entry in entries]

    entriesJSONFile.close()

    with open('../entries.txt', "w") as entriesTextFile:
        entriesTextFile.writelines(entries)
        entriesTextFile.close()
