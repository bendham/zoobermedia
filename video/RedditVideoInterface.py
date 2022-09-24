import praw
from .RedditVideo import RedditVideo
from .VideoHandler import VideoHandler
import requests
from .secrets import reddit_secret, reddit_id
from settings import *
import subprocess
from .Helpers import setAttemptTo


class RedditVideoInterface:

    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    

    def __init__(self, subredditString, maxVids):

        self.redditInstance = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent='my user agent')

        self.url = "https://www.reddit.com"
        self.vidUrlAppear = "v.redd.it"
        self.subredditString = subredditString
        self.sub = self.setSub(subredditString)

        self.vidHandler = VideoHandler()
        self.MAX_VIDEOS = maxVids

    def setSub(self, subreddit):
       return self.redditInstance.subreddit(subreddit)


    def generateVideoList(self):
        self.populateList()
        self.removeUnusable()
        self.processVideos()
        self.getThumbnail()
        self.concat()

        setAttemptTo('success')

    def populateList(self):
        vidNumber = 1

        for submission in self.sub.hot(limit=self.MAX_VIDEOS):
        
            if self.vidUrlAppear in submission.url:
                
                directLink = self.url + submission.permalink

                newVideo = RedditVideo(directLink, vidNumber)
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
    
        for vid in self.vidHandler.vidArray:

            self.downloadVid(vid)
            self.processVidAndRemove(vid)            

    def downloadVid(self, vid):
        print(f"Downloading video #{vid.vidNum}...\n")
        
        videoReq = self.vidHandler.urlRequest(vid.videoUrl)
        self.vidHandler.writeContentFromRequest(videoReq, vid.videoFileDir)

        auddioReq = self.vidHandler.urlRequest(vid.audioUrl)
        self.vidHandler.writeContentFromRequest(auddioReq, vid.audioFileDir)

        #print(videoReq.headers)

    def processVidAndRemove(self, vid):
        print(f"Processing video #{vid.vidNum}...\n")

        sizeVideo = os.stat(vid.videoFileDir).st_size
        if(sizeVideo > 1000):
            self.vidHandler.thumbnail.checkCandidateForThumbnail(vid.videoFileDir)

            # Normalize Audio
            subprocess.call(f'ffmpeg-normalize {vid.audioFileDir} -o {vid.normAudioFileDir}', shell=True)

            # Combine Video and Audio, and add a blurred background
            subprocess.call(f'ffmpeg -hide_banner -loglevel error -i {vid.videoFileDir} -i {vid.normAudioFileDir} -i {WATERMARK_FILE_DIR} -filter_complex "[0]scale=1280:720,setsar=1:1,boxblur=10[bg];[0]scale=-1:720,setsar=16:9[main];[bg][main]overlay=(W-w)/2:(H-h)/2[markit];[markit][2] overlay" {vid.combinedFileDir}', shell=True)

            self.vidHandler.removeFile([vid.videoFileDir, vid.audioFileDir, vid.normAudioFileDir])
        else:
            self.vidHandler.removeFile([vid.videoFileDir, vid.audioFileDir])
            print(f"Video #{vid.vidNum} was too small...")

    def getThumbnail(self):
        self.vidHandler.getThumbnail(True, True)

    def concat(self):
        self.vidHandler.concat()


    

            



        