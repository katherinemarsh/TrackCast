from flask import *
import requests
import json
import xml.etree.cElementTree as ET
from urllib.request import urlopen
from dateutil import parser
from datetime import date

app = Flask(__name__)

url = 'https://gpodder.net'

# creates list containing all podcast info for given data
def makePodList(requestList):
    requestJson = requestList.json();

    # initialize lists for all values parsed from json
    titleList = []
    descriptionList = []
    imgList = []
    feedUrlList = []
    subList = []
    siteList = []
    gpSiteList = []

    for podcast in requestJson:
        for attribute, value in podcast.items():
            if attribute == "url":
                feedUrlList.append(value)
            if attribute == "title":
                titleList.append(value)
            if attribute == "description":
                descriptionList.append(value)
            if attribute == "subscribers":
                subList.append(value)
            if attribute == "scaled_logo_url":
                imgList.append(value)
            if attribute == "website":
                siteList.append(value)
            if attribute == "mygpo_link":
                gpSiteList.append(value)

    # list contains sublists of all needed podcast info
    subPodList = [titleList, imgList, descriptionList, siteList, gpSiteList, feedUrlList, subList]
    return subPodList

# returns list with all podcast info for the current top 25 podcasts
def getTopPodcasts():
    topPodcasts = url + '/toplist/25.json'
    topPodcastsJson = requests.get(topPodcasts)
    topPodList = makePodList(topPodcastsJson)

    return topPodList

# returns list of browse categories and the tags used to search for podcast in each category
def getTopTags():

    # below is result from Jupyter Notebook parse of the api data to determine most popular
    #   tags/best browse categories. View notebook in data folder
    titleList = ["Select a Genre...", "Arts & Entertainment", "Comedy", "News & Politics",
                "Science and Medicine", "Society & Culture", "Technology"]
    tagList = [[""], ["performing-arts", "arts", "arts-entertainment", "literature"], ["comedy"],
                ["news-politics", "news"], ["science-medicine"], ["society-culture", "education"],
                 ["technology", "tech-news", "gadgets", "other-games"]]

    topTagList = [titleList, tagList]
    return topTagList

# returns list containing top 25 podcasts sorted in order of most frequent episode publishes to
#   least frequent
def listenFirst(topPodList):
    daysBwEpList = []

    # the following urls needed to be fixed to prevent 403 errors
    topPodList[5][1] = 'http://feed.thisamericanlife.org/talpodcast?format=xml'
    topPodList[5][9] = 'https://www.engadget.com/rss.xml'
    topPodList[5][18] = 'https://feed.theskepticsguide.org/feed/rss'

    for feedUrl in topPodList[5]:
        tree = ET.ElementTree(file=urlopen(feedUrl))
        root = tree.getroot()

        allDates = []
        for date in root.findall("./channel/item/pubDate"):
            allDates.append(date.text)

        # getting two most recent episode release dates
        allDates = allDates[:50]

        # converting to datetime objects and calculating time difference to determine podcast frequency
        for i in range(len(allDates)):
            allDates[i] = parser.parse(allDates[i])

        sumDiff = 0
        for i in range(len(allDates) - 1):
            sumDiff += (allDates[i] - allDates[i+1]).days

        avgDayDiff = sumDiff / (len(allDates) - 1)

        daysBwEpList.append(avgDayDiff)

    podcastAndFreqList = [topPodList[0], daysBwEpList]

    # sorting in order of most frequent episode publishing to least frequent (days ascending)
    podcastAndFreqList = list(zip(*podcastAndFreqList))
    podcastAndFreqList = sorted(podcastAndFreqList, key=lambda item: item[1])
    podcastAndFreqList = list(zip(*podcastAndFreqList))

    return podcastAndFreqList[0]

userName = ""
passWord = ""

def setLoginInfo(uName, pWord):
    userName = uName
    password = passWord

# returns list of user's podcast subscriptions
def getSubPodcasts(uName, pWord):
    subs = url + '/subscriptions/' + uName + '.json'

    subsJson = requests.get(subs, auth=(uName, pWord))

    subPodList = makePodList(subsJson)
    return subPodList

# list contains all info for the top 25 podcasts to display
topPodList = getTopPodcasts()

# list contains topTags to create browse categories
topTagList = getTopTags()

# list contains titles of most frequent publishing podcast to least frequent
lFList = listenFirst(topPodList)

@app.route('/')
def home():
    return render_template('index.html', topTagList=topTagList, topPodList=topPodList, lFList=lFList)

@app.route('/', methods=["POST"])
def formhandler():
    """Handle the form submission"""

    uName = request.form['username']
    pWord = request.form['password']

    setLoginInfo(uName, pWord)
    subs = url + '/subscriptions/' + uName + '.json'

    subsJson = requests.get(subs, auth=(uName, pWord))

    subPodList = makePodList(subsJson)
    lengthSub = len(subPodList[0])
    return render_template('index.html', topTagList=topTagList, topPodList=topPodList, lFList=lFList, subPodList=subPodList, lengthSub=lengthSub)

@app.route('/search', methods=["POST"])
def searchhandler():
    """Handle the search submission"""

    searchInput = request.form['searchInput']

    search = url + '/search.json?q=' + searchInput

    searchJson = requests.get(search)

    searchList = makePodList(searchJson)
    length = len(searchList[0])

    if (userName != ""):
        subPodList = getSubPodcasts(userName, passWord)
        lengthSub = len(subPodList[0])
    else:
        subPodList = []
        lengthSub = 0
    return render_template('index.html', topTagList=topTagList, topPodList=topPodList, lFList=lFList, subPodList=subPodList, lengthSub = lengthSub, searchResults=searchList, length=length)

@app.route('/browse', methods=["POST"])
def browsehandler():
    browseChoice = request.form['browseChoice']

    tagSearch = []

    for i in range(7):
        if topTagList[0][i] == browseChoice:
            tagSearch = topTagList[1][i]

    titleList = []
    descriptionList = []
    imgList = []
    subList = []

    for i in range(len(tagSearch)):
        browse = url + '/api/2/tag/' + tagSearch[i] + '/100.json'
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

    browsePodList = [titleList, descriptionList, imgList, subList]


    #sort by popularity (subscriber number descending)
    browsePodList = list(zip(*browsePodList))
    browsePodList = sorted(browsePodList, reverse=True, key=lambda item: item[3])
    browsePodList = list(zip(*browsePodList))

    if (userName != ""):
        subPodList = getSubPodcasts(userName, passWord)
        lengthSub = len(subPodList[0])
    else:
        subPodList = []
        lengthSub = 0
    return render_template('index.html', topTagList=topTagList, topPodList=topPodList, lFList=lFList, subPodList=subPodList, lengthSub=lengthSub, browsePodList=browsePodList)

if __name__ == '__main__':
    app.run(debug=True)
