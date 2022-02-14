import sys
from cv2 import exp
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
from selenium.webdriver.support import expected_conditions as EC
from video.RedditComment import RedditComment
from boto3 import Session

from video.RedditCommentSubVid import RedditCommentSubVid
from .secrets import reddit_secret, reddit_id, aws_access_key_id, aws_secret_access_key
from settings import GECKO_DIR
from video.VideoHandler import VideoHandler


class RedditCommentVideoInterface:

    def __init__(self, subIdArray):

        self.redditInstance = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent='my user agent')

        self.session = Session(region_name="ca-central-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.polly = self.session.client("polly")

        self.subIdArray = subIdArray

        self.vidHandler = VideoHandler()


    def generateVideoList(self):
        self.populateList()
        self.concat()

    def populateList(self):
        # Populate array of RedditCommentSubVid
        for id in self.subIdArray:
            subVid = RedditCommentSubVid(id, self.polly, self.redditInstance)
            subVid.generateVideoList()
            self.vidHandler.addVid(subVid.finalSave)

    def buildConcatList(self):
        vidList = []
        for vid in self.vidHandler.vidArray:
            # Add intro to sub???
            vidList.append(vid)

        vidList.append(ZOOBER_OUTRO)
        return vidList

    def concat(self):
        self.vidHandler.concatVidList(self.buildConcatList(), FINAL_SAVE)

