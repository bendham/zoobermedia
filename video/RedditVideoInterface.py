import praw
from .Video import Video
from .VideoHandler import VideoHandler
import requests


class RedditVideoInterface:

    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    MAX_VIDEOS = 2

    def __init__(self, subredditString):

        self.redditInstance = praw.Reddit(client_id='7EnZZe9pViFt7Q', client_secret='z7pn_Jsr0m1iagtaFyuCQpDoXtA', user_agent='my user agent')

        self.url = "https://www.reddit.com"
        self.vidUrlAppear = "v.redd.it"
        self.subredditString = subredditString
        self.sub = self.setSub(subredditString)

        self.vidHandler = VideoHandler()



    def setSub(self, subreddit):
       return self.redditInstance.subreddit(subreddit)


    def generateVideoList(self):
        self.populateList()
        self.removeUnusable()
        self.processVideos()
        self.getThumbnail()

    def populateList(self):
        vidNumber = 1

        for submission in self.sub.hot(limit=self.MAX_VIDEOS):
        
            if self.vidUrlAppear in submission.url:
                
                directLink = self.url + submission.permalink

                newVideo = Video(directLink, vidNumber)
                self.vidHandler.addVid(newVideo)


                vidNumber+=1

    def removeUnusable(self):

        usableVideoHandler = VideoHandler()

        for video in self.vidHandler.vidArray:
            
            json_data = requests.get(video.jsonPostUrl, headers=self.HEADERS).json()


            # Chops json down to a point where some keys beyond this point might be differnet
            jsonDataChop = json_data[0]["data"]["children"][0]["data"]

            # Seperates Crossposts from Non-crossposts because the json format is different
            if "crosspost_parent_list" in jsonDataChop.keys():
                jsonDataChop = jsonDataChop["crosspost_parent_list"][0]

            # If the fallback url exists then bingo was his name-o
            try:
                videoLink = jsonDataChop["secure_media"]["reddit_video"]["fallback_url"]
                video.setVideoAndAudioUrl(videoLink)

                usableVideoHandler.addVid(video)

            except:
                print("Video is not compatable for download. Removing from Video Handler...")

        self.vidHandler = usableVideoHandler

    def processVideos(self):
        self.vidHandler.processVideos()

    def getThumbnail(self):
        self.vidHandler.thumbnail.getFinalThumbs()

            



        