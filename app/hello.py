from flask import *
import pandas as pd
import numpy as np
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

def getTopTags():

    # topTags = url + '/api/2/tags/15.json'
    #
    # topTagsJson = requests.get(topTags)
    #
    # topTagsList = topTagsJson.json();

    titleList = ["Select a Genre...", "Arts & Entertainment", "Comedy", "News & Politics", "Science and Medicine", "Society & Culture", "Technology"]
    tagList = [[""], ["performing-arts", "arts", "arts-entertainment", "literature"], ["comedy"], ["news-politics", "news"], ["science-medicine"],
                  ["society-culture", "education"], ["technology", "tech-news", "gadgets", "other-games"]]

    # for podcast in topTagsList:
    #     for attribute, value in podcast.items():
    #         if attribute == "title":
    #             titleList.append(value)
    #         if attribute == "tag":
    #             tagList.append(value)

    topTagsInfoList = [titleList, tagList]
    return topTagsInfoList

@app.route('/')
def home():
    subscriptions = [0, 0], [0, 0], [0, 0]
    browsePodcastInfo = [0, 0], [0, 0], [0, 0]
    searchPodcastInfo = [0, 0], [0, 0], [0, 0]

    topTagsInfoList = getTopTags()
    return render_template('index.html', subscriptions=subscriptions, lengthCount=0, length=0, topTagsInfoList=topTagsInfoList, browsePodcastInfo=browsePodcastInfo)

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
    browsePodcastInfo = [0, 0], [0, 0], [0, 0]
    searchPodcastInfo = [0, 0], [0, 0], [0, 0]


    topTagsInfoList = getTopTags()

    return render_template('index.html', subscriptions=podcastInfo, lengthCount=lengthCount, searchResults=searchResults, length=0, topTagsInfoList=topTagsInfoList, browsePodcastInfo=browsePodcastInfo)

@app.route('/search', methods=["POST"])
def searchhandler():
    """Handle the search submission"""

    searchInput = request.form['searchInput']

    search = url + '/search.json?q=' + searchInput

    searchJson = requests.get(search)

    searchPodcastInfo = makePodcastArr(searchJson)
    length = len(searchPodcastInfo[0])
    subscriptions = [0, 0], [0, 0], [0, 0]
    browsePodcastInfo = [0, 0], [0, 0], [0, 0]

    topTagsInfoList = getTopTags()

    return render_template('index.html', searchResults=searchPodcastInfo, length=length, lengthCount=0, subscriptions=subscriptions, topTagsInfoList=topTagsInfoList, browsePodcastInfo=browsePodcastInfo)

@app.route('/browse', methods=["POST"])
def browsehandler():
    topTagsInfoList = getTopTags()
    browseChoice = request.form['browseChoice']

    tagSearch = []

    for i in range(7):
        if topTagsInfoList[0][i] == browseChoice:
            tagSearch = topTagsInfoList[1][i]

    browsePodcastInfo = []
    titleList = []
    descriptionList = []
    imgList = []
    subList = []

    for i in range(len(tagSearch)):
        browse = url + '/api/2/tag/' + tagSearch[i] + '/20.json'
        browseList = requests.get(browse)
        browseJson = browseList.json()

        for podcast in browseJson:
            for attribute, value in podcast.items():
                if attribute == "title":
                    titleList.append(value)
                if attribute == "description":
                    descriptionList.append(value)
                if attribute == "scaled_logo_url":
                    imgList.append(value)
                if attribute == "subscribers":
                    subList.append(value)

    browsePodcastInfo = [titleList], [descriptionList], [imgList], [subList]
    return str(browsePodcastInfo)

    #sort by popularity (subscriber number descending)
    browsePodcastInfo = zip(*browsePodcastInfo)
    browsePodcastInfo.sort(key=lambda item: item[3])
    browsePodcastInfo = zip(*browsePodcastInfo)
    return str(browsePodcastInfo)

    subscriptions = [0, 0], [0, 0], [0, 0]
    searchPodcastInfo = [0, 0], [0, 0], [0, 0]
    topTagsInfoList = getTopTags()

    # just need to implement below!
    return render_template('index.html', searchResults=searchPodcastInfo, length=0, lengthCount=0, subscriptions=subscriptions, topTagsInfoList=topTagsInfoList, browsePodcastInfo=browsePodcastInfo)

if __name__ == '__main__':
    app.run(debug=True)
