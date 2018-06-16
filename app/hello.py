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
    """Handle the search submission"""

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

    def getTopTags():
        url = 'https://gpodder.net';
        search = url + '/search.json?q=' + searchInput

        searchJson = requests.get(search)

        searchList = searchJson.json();

        titleList = []
        descriptionList = []

    def topListHandler():
        """Handle the top 25 podcast display"""

        url = 'https://gpodder.net';
        top = url + '/toplist/25.json'

        topJson = requests.get(top)

        topList = searchJson.json();

        titleList = []
        descriptionList = []
        imgList = []

        for podcast in topList:
            for attribute, value in podcast.items():
                if attribute == "title":
                    titleList.append(value)
                if attribute == "description":
                    descriptionList.append(value)
                if attribute == "scaled_logo_url":
                    imgList.append(value)


        topPodcastInfo = [titleList, imgList, descriptionList]
        lengthTop = 25
        subscriptions = [0, 0], [0, 0], [0, 0]
        # just need to implement below!
        return render_template('index.html', searchResults=searchPodcastInfo, length=length, lengthCount=0, subscriptions=subscriptions)

    def browseHandler():
        """Handle the browse option"""

        browseInput = request.form['browseInput']

        url = 'https://gpodder.net';
        browse = url + '/api/2/tag/' + browseInput + '/25.json'

        browseJson = requests.get(browse)

        browseList = browseJson.json();

        titleList = []
        descriptionList = []
        imgList = []
        subList = []

        for podcast in browseList:
            for attribute, value in podcast.items():
                if attribute == "title":
                    titleList.append(value)
                if attribute == "description":
                    descriptionList.append(value)
                if attribute == "subscribers":
                    subList.append(value)
                if attribute == "scaled_logo_url":
                    imgList.append(value)


        browsePodcastInfo = [titleList, imgList, descriptionList, subList]

        #sort by popularity (subscriber number descending)
        sorted(browsePodcastInfo, key=lambda item: item[3])

        lengthBrowse = 25
        subscriptions = [0, 0], [0, 0], [0, 0]
        # just need to implement below!
        return render_template('index.html', searchResults=searchPodcastInfo, length=length, lengthCount=0, subscriptions=subscriptions)


if __name__ == '__main__':
    app.run(debug=True)
