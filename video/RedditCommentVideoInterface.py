import praw
from praw.models import base
import requests
from settings import *
import subprocess
import pyttsx3
from praw.reddit import Submission
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from video.RedditComment import RedditComment
from boto3 import Session
from .secrets import reddit_secret, reddit_id, aws_access_key_id, aws_secret_access_key
from settings import GECKO_DIR
from video.VideoHandler import VideoHandler


class RedditCommentVideoInterface:

    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    MAX_VIDEOS = 3
    SILENCE_TIME = 0.75 # 0.75 s pause between comment reading

    def __init__(self):

        self.redditInstance = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent='my user agent')

        self.url = "https://www.reddit.com"
        self.vidUrlAppear = "v.redd.it"
        self.comments = []

        self.session = Session(region_name="ca-central-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.polly = self.session.client("polly")

        self.vidHandler = VideoHandler()

        self.concatVidListDir = os.path.join(COMMENT_FINAL_VIDEO_DIR, "concat.txt")


    def generateVideoList(self):
        self.populateList()
        self.removeUnusable()
        self.makeVideos()


    def populateList(self):
        subMis = self.redditInstance.submission(id="iwedc5")

        drv = self.setUpRedditPage(subMis)

        for idx, comment in enumerate(subMis.comments[1:3]):
            cmt = RedditComment(self.polly, drv, comment, idx+1)
            cmt.populateChildComments()
            cmt.buildVideoFrames2()

            if(cmt.goodToUse):
                self.comments.append(cmt)

        drv.quit()

    def removeUnusable(self):
        "This processing is already done when making the comments, the goodToUse boolean"
        
    def makeVideos(self):

        # Process audio
        self.processAudio()
        # Process video and get rid of temp files
        self.processVideoAndCleanUp()
        # Combine in one
        self.concat()
        # Get rid of files used in concat
        self.cleanUpFilesForConcat()

    def processAudio(self):
        for comment in self.comments:
            if(comment.goodToUse == True): # Add case for no child
                concatFileDir = comment.concatFileDir.replace("\\", "/") # Bug in FFMPEG where \ is not good for input file
                with open(concatFileDir, 'w') as f:
                    f.write(f"file '{comment.name}.mp3'\n")
                    for child in comment.childComments:
                        f.write(f"file 'silence075.mp3'\n")
                        f.write(f"file '{child.name}.mp3'\n")

            subprocess.call(f'ffmpeg -f concat -safe 0 -i {concatFileDir} -c copy {comment.concatAudioFilePath}', shell=True)

    def processVideoAndCleanUp(self):
        for comment in self.comments:
            if(len(comment.childComments)==0):
                ffmpegCommand = f"ffmpeg -loop 1 -y -i {comment.commentFrameDir} -i {comment.concatAudioFilePath} -shortest {comment.finalSave}"
            else:
                inputString = f"-i {comment.commentFrameDir}"


                filterString=""

                prevTemp = "0:v"
                durationToWait = comment.dur + self.SILENCE_TIME # SILENCE_TIME seconds of silence
                for idx, child in enumerate(comment.childComments):
                    inputString += f" -i {child.commentFrameDir}"

                    filterString += f"[{prevTemp}][{idx+1}:v] overlay=0:0:enable='gte(t,{durationToWait})'"
                    if(idx != len(comment.childComments)-1):
                        filterString += f"[tmp{idx+1}];"


                    durationToWait += child.dur + self.SILENCE_TIME
                    prevTemp = f"tmp{idx+1}"

                ffmpegCommand = f'ffmpeg -loop 1 -y {inputString} -i {comment.concatAudioFilePath} -filter_complex "{filterString}" -shortest {comment.finalSave}'

            
            subprocess.call(ffmpegCommand, shell=True)

            self.vidHandler.addVid(comment.finalSave)

            self.cleanupCommentFiles(comment)

    def cleanUpFilesForConcat(self):
        for comment in self.comments:
            os.remove(comment.finalSave)

    def cleanupCommentFiles(self, cmt: RedditComment):
        os.remove(cmt.commentFrameDir)
        os.remove(cmt.pngPath)
        os.remove(cmt.mp3Path)
        os.remove(cmt.concatFileDir)
        os.remove(cmt.concatAudioFilePath)
        
        for child in cmt.childComments:
            os.remove(child.commentFrameDir)
            os.remove(child.pngPath)
            os.remove(child.mp3Path)
    
    def buildConcatText(self):
        with open(self.concatVidListDir, 'w') as f:
            for comment in self.comments:
                f.write(f"file '{comment.name}.mp4'\n")
                if(comment != self.comments[-1]):
                    f.write(f"file cut75fps.mp4\n")

    def concat(self):
        self.buildConcatText()
        self.vidHandler.concatFFmpeg(self.concatVidListDir)

    def setUpRedditPage(self, subMission: Submission):

        cmts = "https://www.reddit.com" + subMission.permalink
        print(cmts)

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.set_preference("dom.push.enabled", False)  # kill notification popup
        ser = Service(GECKO_DIR)
        drv = Firefox(options=opts, service=ser)
        drv.execute_script("document.body.style.zoom='250%'")
        
        drv.get(cmts)
        profile_btn = drv.find_element(By.ID, "USER_DROPDOWN_ID")
        profile_btn.click()
        night_mode_btn = drv.find_element(By.XPATH, "//div[@role='menu']/button")
        night_mode_btn.click()

        return drv