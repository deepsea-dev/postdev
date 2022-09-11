from flask import Flask, render_template, request
import re
from aitextgen import aitextgen
ai = aitextgen(model_folder=".", to_gpu=False)

def generateProjects():
  generated = []
  while len(generated) < 10:
    line = ai.generate_one().rstrip()
    print(line)
    match = re.search(r"(True|False) \| \d+ \| \d+ \| .*? \| .*", line)
    if match == None: continue

    values = line.split("|")
    generated.append({
      "title": values[3],
      "tagline": values[4],
      "winner": values[0],
      "likes": values[1],
      "comments": values[2]
    })

  return generated


app = Flask(__name__)

@app.route('/')
def index():
  onlyWinners = request.args.get('winners', default=False, type=lambda v: v.lower() == 'true')
  projects = generateProjects()
  return render_template('index.html', projects=projects, onlyWinners=onlyWinners)