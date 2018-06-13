from flask import *
import pandas as pd
import requests
import json

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def formhandler():
    """Handle the form submission"""

    uName = request.form['username']
    pWord = request.form['password']

    url = 'https://gpodder.net';
    subs = url + '/subscriptions/' + uName + '.json';

    subsJson = requests.get(subs, auth=(uName, pWord))

    subsList = subsJson.json();

    titleList = []
    descriptionList = []
    imgList = []

    for podcast in subsList:
        for attribute, value in podcast.items():
            if attribute == "title":
                titleList.append(value)
            if attribute == "description":
                descriptionList.append(value)
            if attribute == "scaled_logo_url":
                imgList.append(value)


    podcastInfo = [titleList, descriptionList, imgList]

    return add_subs_page(podcastInfo)

def add_subs_page(podcastInfo):
    return render_template('index.html', subscriptions=podcastInfo, test=5)

if __name__ == '__main__':
    app.run(debug=True)
from flask import *
import pandas as pd
import requests
import json

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def formhandler():
    """Handle the form submission"""

    uName = request.form['username']
    pWord = request.form['password']

    url = 'https://gpodder.net';
    subs = url + '/subscriptions/' + uName + '.json';

    subsJson = requests.get(subs, auth=(uName, pWord))

    subsList = subsJson.json();

    titleList = []
    descriptionList = []
    imgList = []

    for podcast in subsList:
        for attribute, value in podcast.items():
            if attribute == "title":
                titleList.append(value)
            if attribute == "description":
                descriptionList.append(value)
            if attribute == "scaled_logo_url":
                imgList.append(value)


    podcastInfo = [titleList, descriptionList, imgList]

    return add_subs_page(podcastInfo)

def add_subs_page(podcastInfo):
    return render_template('index.html', subscriptions=podcastInfo, test=5)

if __name__ == '__main__':
    app.run(debug=True)
