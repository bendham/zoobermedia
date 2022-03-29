from praw.reddit import Comment
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import BACKGROUND_FILE_DIR, COMMENT_PNG_DIR, COMMENT_MP3_DIR, COMMENT_PNG_FRAME_DIR, COMMENT_FINAL_VIDEO_DIR, COMMENT_FINAL_AUDIO_DIR
import os
from PIL import Image, ImageOps
from moviepy.editor import AudioFileClip
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from video.RedditCommentImage import RedditCommentImage
from praw.models import MoreComments
from video.Helpers import *
from selenium.webdriver.common.action_chains import ActionChains
import math


class RedditComment:

    PERCENT_TO_BEAT = 0.3
    MAX_CHILD_COMMENTS = 4
    COMMENT_WIDTH = 1024
    MAX_AMOUNT_OF_WORDS = 60

    timeout = 20
    goodToUse = False

    totalVidDuration = 0

    h = 0
    w = 0

    def __init__(self, speechEngine, drv: WebDriver, com: Comment, identifier, url) -> None:
        self.urlToUse = url
        self.com = com
        self.drv = drv
        self.identifier = f"{identifier}_"
        self.speechEngine = speechEngine
        self.childComments = []

        self.name = self.identifier + self.getId()

        self.pngPath = os.path.join(COMMENT_PNG_DIR, self.name + ".png")
        self.mp3Path = os.path.join(COMMENT_MP3_DIR, self.name + ".mp3")
        self.finalSave = os.path.join(COMMENT_FINAL_VIDEO_DIR, self.name + ".mp4")

        self.concatFileDir = os.path.join(COMMENT_MP3_DIR, f'{self.name}.txt')
        self.concatAudioFilePath = os.path.join(COMMENT_FINAL_AUDIO_DIR, f'concat_{self.name}.mp3')


        self.screenShotAndMp3()


    def __str__(self) -> str:
        return f"CommentId: {self.getId()}, PngPath: {self.pngPath}, Mp3Path: {self.mp3Path}"

    def screenShotAndMp3(self):
        try:
            cmt = WebDriverWait(self.drv, 10*self.timeout).until(EC.visibility_of_element_located((By.ID, self.getElmId())))
            self.drv.execute_script("arguments[0].scrollIntoView();", cmt)
            WebDriverWait(self.drv, 10*self.timeout).until(EC.visibility_of_element_located((By.XPATH, f"//div[@id='{self.getElmId()}']/div[2]/div/a[@data-testid='comment_author_icon']")))
            cmt = WebDriverWait(self.drv, 10*self.timeout).until(EC.visibility_of_element_located((By.ID, self.getElmId())))
            
        except TimeoutException:
            print("Page load timed out, will not use this comment...")
            self.goodToUse = False
        else:
            self.goodToUse = True
            cmt.screenshot(self.pngPath)
        
        if(self.goodToUse == True):
            hasAudio = requestAudio(self.speechEngine, self.mp3Path, self.com.body, "Matthew")

            if(hasAudio):
                audioclip = AudioFileClip(self.mp3Path)
                self.dur = audioclip.duration
                audioclip.close()
            else:
                self.goodToUse = False

    def populateChildComments(self):
        isStillGoodComments = True
        clickedContinueThread = False
        commentCount = 1
        compareScore = self.com.score

        replies = self.com.replies
        if(len(replies)): # Is this right?
            child = self.com.replies[0]
            threadId = child.id
            if(type(child)==MoreComments): # I dont deal with this case for right now...
                isStillGoodComments = False
        else:
            isStillGoodComments = False

        while(isStillGoodComments):
            if(child.score/compareScore >= self.PERCENT_TO_BEAT and commentCount < self.MAX_CHILD_COMMENTS):
                if(len(child.body.split(" ")) < self.MAX_AMOUNT_OF_WORDS):

                    if(commentCount == 2):
                        try:
                            # Is this the problem?
                            threadElm = WebDriverWait(self.drv, self.timeout).until(
                            lambda x: x.find_element(By.XPATH, f"//div[@id='continueThread-t1_{threadId}']/div[2]/a"))
                            
                            threadElm.click()

                            newCmt = WebDriverWait(self.drv, 10*self.timeout).until(EC.visibility_of_element_located((By.ID, f"t1_{child.id}")))
            
                            self.drv.execute_script("arguments[0].scrollIntoView();", newCmt)
                            
                        except TimeoutException:
                            isStillGoodComments = False
                            print("Page load timed out, could not continue the thread...")
                            break
                        else:
                            clickedContinueThread = True

                    redditChildComment = RedditComment(self.speechEngine, self.drv, child, self.identifier + str(commentCount), self.urlToUse)
                    if(redditChildComment.goodToUse == True):
                        self.childComments.append(redditChildComment)
                        compareScore = child.score
                        child = child.replies[0]

                        commentCount += 1
                    else: # Maybe add
                        isStillGoodComments = False
                else:
                    isStillGoodComments = False
            else:
                isStillGoodComments = False

        if(clickedContinueThread):
            self.drv.execute_script("window.history.go(-1)")
            #self.drv.get(self.urlToUse)

    def resizeCommentImage(self, scaleFactor):
        f1 = Image.open(self.pngPath)
        self.w, self.h = f1.size

        self.h = math.floor(scaleFactor*self.h)
        self.w = math.floor(scaleFactor*self.w)

        #f1 = f1.resize((self.w, self.h), Image.ANTIALIAS)

        f1 = ImageOps.fit(f1, (self.w, self.h))

        return f1

    def buildVideoFrames(self):

        bgBase = Image.open(BACKGROUND_FILE_DIR)
        bgX, bgY = bgBase.size

        
        
        totalCommentHeight = 0
        commentList = []
        commentImg = RedditCommentImage(self)
        commentList.append(commentImg)
        totalCommentHeight += commentImg.h
        for comment in self.childComments:
            if(comment.goodToUse): # There has to be a better way
                commentImg = RedditCommentImage(comment)
                commentList.append(commentImg)
                totalCommentHeight += commentImg.h
            else:
                break
                
        totalHeightSpace = bgY*0.8
        scaleFactor = totalHeightSpace/totalCommentHeight
        usedScaleFactor = scaleFactor

        if(scaleFactor*commentList[0].w > bgX):
            usedScaleFactor = (bgX*0.95)/commentList[0].w

        newTotalHeight = 0
        for comment in commentList:
            newTotalHeight += comment.h*usedScaleFactor

        prevCommentH = 0
        hOffset = 0
        for idx, comment in enumerate(commentList):
            
            f1 = comment.resizeCommentImage(usedScaleFactor)
            bgBase.paste(f1, ((bgX-f1.width)//2, math.floor((bgY-newTotalHeight)//2 + hOffset)))
            comment.redditComment.commentFrameDir = os.path.join(COMMENT_PNG_FRAME_DIR, f"f{str(idx+1)}_{self.getId()}.png")
            bgBase.save(os.path.join(COMMENT_PNG_FRAME_DIR, comment.redditComment.commentFrameDir))

            prevCommentH = f1.height

            hOffset += prevCommentH

    # def buildVideoFrames(self):

    #     bgBase = Image.open(BACKGROUND_FILE_DIR)
    #     bgX, bgY = bgBase.size

    #     hOffset = (bgY-self.h)/8 # check
        
    #     totalCommentHeight = 0
    #     commentList = []
    #     commentImg = RedditCommentImage(self)
    #     commentList.append(commentImg)
    #     totalCommentHeight += commentImg.h
    #     for comment in self.childComments:
    #         if(comment.goodToUse): # There has to be a better way
    #             commentImg = RedditCommentImage(comment)
    #             commentList.append(commentImg)
    #             totalCommentHeight += commentImg.h
    #         else:
    #             break

    #     wOffset = (bgX-commentList[0].w)/2
    #     rescaleHeightFactor = (bgY - hOffset)/totalCommentHeight

    #     if(rescaleHeightFactor*commentList[0].w > bgX):
    #         rescaleHeightFactor = (bgX-wOffset)//commentList[0].w

    #     prevCommentH = hOffset
    #     for idx, comment in enumerate(commentList):
    #         f1 = comment.resizeCommentImage(rescaleHeightFactor)
    #         bgBase.paste(f1, ((bgX-comment.w)//2, math.floor(hOffset)))
    #         comment.redditComment.commentFrameDir = os.path.join(COMMENT_PNG_FRAME_DIR, f"f{str(idx+1)}_{self.getId()}.png")
    #         bgBase.save(os.path.join(COMMENT_PNG_FRAME_DIR, comment.redditComment.commentFrameDir))

    #         prevCommentH = comment.h
    #         hOffset += prevCommentH

    def getId(self):
        return self.com.id

    def getElmId(self):
        return f"t1_{self.com.id}"

