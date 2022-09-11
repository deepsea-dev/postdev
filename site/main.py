from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def index():
  projects = [
    {
      "title": "Octocatch",
      "tagline": "collect falling items at the bottom of the ocean as an octopus",
      "winner": True,
      "likes": "8453",
      "comments": "7895"}
  ] * 6

  projects += [
    {
      "title": "Octocatch",
      "tagline": "collect falling items at the bottom of the ocean as an octopus",
      "winner": False,
      "likes": "8453",
      "comments": "7895"}
  ] * 6
  return render_template('index.html', projects=projects)