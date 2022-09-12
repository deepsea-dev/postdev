# postdev - the mirror of devpost
A gpt-2 powered hackathon project idea generator. With devpost you dev then post, but these are posts for you to dev. We even predict if the projects are going to win.

![a orange accented dark themed website with a grid of hackathon projects](/screenshot.png)

[![Generate page content](https://github.com/deepsea-dev/postdev/actions/workflows/static.yml/badge.svg)](https://github.com/deepsea-dev/postdev/actions/workflows/static.yml)

## how it works
Our project uses data scraped from devpost’s most popular projects. We used [aitextgen](https://github.com/minimaxir/aitextgen), a gpt2 library for training our model and producing sample projects. Using **15,000** devpost submissions, we fine-tuned the model to produce similar ones. For each project we generate a title, tagline, number of likes, and number of comments.


Rather than a traditional backend, we use a funky custom Github action to periodically run a python script to generate new submissions with this model and convert them into a json file. The action also downloads images from pixabay using the project title as a prompt. The action then copies this generated content into the site folder and then publishes this on Github pages.

## repository map
scraper: scrapes devpost to gather project information
Mapper: takes the scraped devpost information and maps to a text file that can be used to train the ai
generator: runs the model to generate the projects and download images
site: a website to view the projects

For each python script first use
`pipenv install`
and then
`pipenv run python <script_name>.py`

## whats next
Use more training data, we were limited by time here and our free gpu hours on google colab. This would improve the quality of predictions.
