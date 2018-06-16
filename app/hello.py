from flask import *
import pandas as pd
import requests
import json

app = Flask(__name__)

url = 'https://gpodder.net'

def makePodcastArr(requestList):
    requestJson = requestList.json();

    titleList = []
    descriptionList = []
    imgList = []

    for podcast in requestJson:
        for attribute, value in podcast.items():
            if attribute == "title":
                titleList.append(value)
            if attribute == "description":
                descriptionList.append(value)
            if attribute == "scaled_logo_url":
                imgList.append(value)


    podcastInfo = [titleList, imgList, descriptionList]
    return podcastInfo

@app.route('/')
def home():
    subscriptions = [0, 0], [0, 0], [0, 0]
    return render_template('index.html', subscriptions=subscriptions, lengthCount=0, length=0)

@app.route('/', methods=["POST"])
def formhandler():
    """Handle the form submission"""

    uName = request.form['username']
    pWord = request.form['password']

    subs = url + '/subscriptions/' + uName + '.json'

    subsJson = requests.get(subs, auth=(uName, pWord))

    podcastInfo = makePodcastArr(subsJson)
    lengthCount = len(podcastInfo[0])
    searchResults = [0, 0], [0, 0], [0, 0]

    return render_template('index.html', subscriptions=podcastInfo, lengthCount=lengthCount, searchResults=searchResults, length=0)

@app.route('/search', methods=["POST"])
def searchhandler():
    """Handle the search submission"""

    searchInput = request.form['searchInput']

    search = url + '/search.json?q=' + searchInput

    searchJson = requests.get(search)

    searchPodcastInfo = makePodcastArr(searchJson)
    length = len(searchPodcastInfo[0])
    subscriptions = [0, 0], [0, 0], [0, 0]
    return render_template('index.html', searchResults=searchPodcastInfo, length=length, lengthCount=0, subscriptions=subscriptions)

if __name__ == '__main__':
    app.run(debug=True)
