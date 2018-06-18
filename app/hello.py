from flask import *
import requests
import json
import xml.etree.cElementTree as ET
import urllib2
from dateutil import parser
from datetime import date

app = Flask(__name__)

url = 'https://gpodder.net'

def makePodcastArr(requestList):
    requestJson = requestList.json();

    titleList = []
    descriptionList = []
    imgList = []
    feedUrlList = []

    for podcast in requestJson:
        for attribute, value in podcast.items():
            if attribute == "title":
                titleList.append(value)
            if attribute == "description":
                descriptionList.append(value)
            if attribute == "scaled_logo_url":
                imgList.append(value)
            if attribute == "url":
                feedUrlList.append(value)


    podcastInfo = [titleList, imgList, descriptionList, feedUrlList]
    return podcastInfo

def getTopTags():

    # topTags = url + '/api/2/tags/15.json'
    # topTagsJson = requests.get(topTags)
    # topTagsList = topTagsJson.json();

    #above api request was not sorted by most popular tags
    #below is hand picked result from Jupyter Notebook parse of the api data in an attempt to use most popular tags
    titleList = ["Select a Genre...", "Arts & Entertainment", "Comedy", "News & Politics", "Science and Medicine", "Society & Culture", "Technology"]
    tagList = [[""], ["performing-arts", "arts", "arts-entertainment", "literature"], ["comedy"], ["news-politics", "news"], ["science-medicine"],
                  ["society-culture", "education"], ["technology", "tech-news", "gadgets", "other-games"]]

    topTagsInfoList = [titleList, tagList]
    return topTagsInfoList

def getTopPodcasts():

    topPodcasts = url + '/toplist/25.json'

    topPodcastsJson = requests.get(topPodcasts)

    topPodcastsInfoList = makePodcastArr(topPodcastsJson)

    return topPodcastsInfoList

def listenFirst(topPodcastsInfoList):
    daysBwEpList = []

    # the following urls needed to be fixed to prevent 403 errors
    topPodcastsInfoList[3][1] = 'http://feed.thisamericanlife.org/talpodcast?format=xml'
    topPodcastsInfoList[3][9] = 'https://www.engadget.com/rss.xml'
    topPodcastsInfoList[3][18] = 'https://feed.theskepticsguide.org/feed/rss'


    for feedUrl in topPodcastsInfoList[3]:
        # hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        tree = ET.ElementTree(file=urllib2.urlopen(feedUrl))
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

    # below list contains:
    # row 0-2 - title, desc, and img of top 25 podcast titles
    # row 3 - frequency of episode release for each of these podcasts in days
    podcastAndFreqList = [topPodcastsInfoList[0], topPodcastsInfoList[1], topPodcastsInfoList[2], topPodcastsInfoList[3], daysBwEpList]

    #sorting in order of most frequent to least frequent (days ascending)
    podcastAndFreqList = zip(*podcastAndFreqList)
    podcastAndFreqList.sort(key=lambda item: item[4])
    podcastAndFreqList = zip(*podcastAndFreqList)
    return podcastAndFreqList

def mostRecent(topPodcastsInfoList):
    daysBwEpList = []
    feedUrlList = topPodcastsInfoList[3]

    # the following were causing http 403 errors
    feedUrlList.remove('http://feeds.thisamericanlife.org/talpodcast')
    feedUrlList.remove('http://podcasts.engadget.com/rss.xml')
    feedUrlList.remove('http://www.theskepticsguide.org/feed/rss.aspx?feed=SGU')


    for feedUrl in feedUrlList:
        tree = ET.ElementTree(file=urllib2.urlopen(feedUrl))
        root = tree.getroot()

        allDates = []
        for date in root.find("./channel/item/pubDate"):
            allDates.append(date.text)

    # converting to datetime objects and calculating time difference to determine podcast frequency
    for i in range(len(allDates)):
        allDates[i] = parser.parse(allDates[i])

    # below list contains:
    # row 0-2 - title, desc, and img of top 25 podcast titles
    # row 3 - frequency of episode release for each of these podcasts in days
    podcastAndFreqList = [topPodcastsInfoList[0], topPodcastsInfoList[1], topPodcastsInfoList[2], topPodcastsInfoList[3], daysBwEpList]

    #sorting in order of most frequent to least frequent (days ascending)
    podcastAndFreqList = zip(*podcastAndFreqList)
    podcastAndFreqList.sort(key=lambda item: item[4])
    podcastAndFreqList = zip(*podcastAndFreqList)
    return podcastAndFreqList
@app.route('/')
def home():
    topPodcastsInfoList = getTopPodcasts()
    topTagsInfoList = getTopTags()
    return str(listenFirst(topPodcastsInfoList))
    return render_template('index.html', topTagsInfoList=topTagsInfoList, topPodcastsInfoList=topPodcastsInfoList)

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

    return render_template('index.html', subscriptions=podcastInfo, lengthCount=lengthCount, topTagsInfoList=topTagsInfoList)

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

    return render_template('index.html', searchResults=searchPodcastInfo, length=length, lengthCount=0, subscriptions=subscriptions, topTagsInfoList=topTagsInfoList)

@app.route('/browse', methods=["POST"])
def browsehandler():
    topTagsInfoList = getTopTags()
    browseChoice = request.form['browseChoice']

    tagSearch = []

    for i in range(7):
        if topTagsInfoList[0][i] == browseChoice:
            tagSearch = topTagsInfoList[1][i]

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

    browsePodcastInfo = [titleList, descriptionList, imgList, subList]
    #sort by popularity (subscriber number descending)

    browsePodcastInfo = zip(*browsePodcastInfo)
    browsePodcastInfo.sort(reverse=True, key=lambda item: item[3])
    browsePodcastInfo = zip(*browsePodcastInfo)

    subscriptions = [0, 0], [0, 0], [0, 0]
    searchPodcastInfo = [0, 0], [0, 0], [0, 0]
    topTagsInfoList = getTopTags()

    # just need to implement below!
    return render_template('index.html', lengthCount=0, subscriptions=subscriptions, topTagsInfoList=topTagsInfoList, browsePodcastInfo=browsePodcastInfo)

if __name__ == '__main__':
    app.run(debug=True)
