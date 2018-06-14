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


    podcastInfo = [titleList, imgList, descriptionList]
    lengthCount = len(podcastInfo[0])

    return render_template('index.html', subscriptions=podcastInfo, lengthCount=lengthCount)

@app.route('/search', methods=["POST"])
def searchhandler():
    """Handle the form submission"""

    searchInput = request.form['search']

    url = 'https://gpodder.net';
    search = url + '/search.json';

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


    searchPodcastInfo = [titleList, descriptionList, imgList]
    length = len(searchPodcastInfo[0])

    return add_search_page(searchPodcastInfo, length)

def add_search_page(searchPodcastInfo, length):
    return render_template('index.html', searchResults=searchPodcastInfo, length=5)

if __name__ == '__main__':
    app.run(debug=True)
