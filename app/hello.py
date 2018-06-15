from flask import *
import pandas as pd
import requests
import json

app = Flask(__name__)
@app.route('/')
def home():
    subscriptions = [0, 0], [0, 0], [0, 0]
    return render_template('index.html', subscriptions=subscriptions, lengthCount=0, length=0)

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


    podcastInfo = [titleList, imgList, descriptionList]
    lengthCount = len(podcastInfo[0])
    searchResults = [0, 0], [0, 0], [0, 0]

    return render_template('index.html', subscriptions=podcastInfo, lengthCount=lengthCount, searchResults=searchResults, length=0)

@app.route('/search', methods=["POST"])
def searchhandler():
    """Handle the form submission"""

    searchInput = request.form['searchInput']

    url = 'https://gpodder.net';
    search = url + '/search.json?q=' + searchInput

    searchJson = requests.get(search)

    searchList = searchJson.json();

    titleList = []
    descriptionList = []
    imgList = []

    for podcast in searchList:
        for attribute, value in podcast.items():
            if attribute == "title":
                titleList.append(value)
            if attribute == "description":
                descriptionList.append(value)
            if attribute == "scaled_logo_url":
                imgList.append(value)


    searchPodcastInfo = [titleList, imgList, descriptionList]
    length = len(searchPodcastInfo[0])
    subscriptions = [0, 0], [0, 0], [0, 0]
    return render_template('index.html', searchResults=searchPodcastInfo, length=length, lengthCount=0, subscriptions=subscriptions)

if __name__ == '__main__':
    app.run(debug=True)
