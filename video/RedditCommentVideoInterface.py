from cv2 import exp
import praw
from settings import *

from boto3 import Session
from types import SimpleNamespace

from video.RedditCommentSubVid import RedditCommentSubVid
from .secrets import reddit_secret, reddit_id, aws_access_key_id, aws_secret_access_key
from settings import GECKO_DIR
from video.VideoHandler import VideoHandler


class RedditCommentVideoInterface:

    def __init__(self, video_to_make_info):

        self.redditInstance = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent='my user agent')

        self.session = Session(region_name="ca-central-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.polly = self.session.client("polly")

        self.subIdArray = video_to_make_info['subreddit']
        self.sectionsPerSub = video_to_make_info['commentSubreddits']

        self.vidHandler = VideoHandler(video_to_make_info)


    def generateVideoList(self):
        self.populateList()
        self.concat()
        self.vidHandler.addBackground(FINAL_SAVE_TEMP, FINAL_SAVE)
        # setAttemptTo('success')

    def cleanUp(self):

        os.remove(FINAL_SAVE_TEMP)
        self.vidHandler.clean_up()

    def populateList(self):
        # Populate array of RedditCommentSubVid
        for id in self.subIdArray:
            subVid = RedditCommentSubVid(id, self.polly, self.redditInstance, self.sectionsPerSub)
            subVid.generateVideoList()

            vidObj = SimpleNamespace(finalSave=subVid.introVidPath, name=subVid.introVidName)
            self.vidHandler.addVid(vidObj)
            self.vidHandler.addVid(subVid)

    def buildConcatList(self):
        vidObj = SimpleNamespace(finalSave=ZOOBER_OUTRO)
        self.vidHandler.addVid(vidObj)
        return self.vidHandler.vidArray

    def buildConcatText(self):
        with open(FINAL_CONCAT_VID_LIST_FILE, 'w') as f:
            for vid in self.vidHandler.vidArray:
                f.write(f"file '{vid.name}'\n")

    def concat(self):
        self.buildConcatText()
        self.vidHandler.concatFFmpeg(FINAL_CONCAT_VID_LIST_FILE, FINAL_SAVE_TEMP)
        # self.vidHandler.concatVidList(self.buildConcatList(), FINAL_SAVE, hasOutro=True)

    
