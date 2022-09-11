from flask import Flask

app = Flask('postdev')

@app.route('/')
def index():
  return "hello world"