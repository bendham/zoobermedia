from re import S
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

    def __init__(self, speechEngine, drv: WebDriver, com: Comment, identifier) -> None:
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
            cmt = WebDriverWait(self.drv, self.timeout).until(
            lambda x: x.find_element(By.ID, self.getElmId()))
        except TimeoutException:
            print("Page load timed out, will not use this comment...")
        else:
            self.goodToUse = True
            cmt.screenshot(self.pngPath)
        
        if(self.goodToUse == True):
            hasAudio = self.requestAudio()

            if(hasAudio):
                audioclip = AudioFileClip(self.mp3Path)
                self.dur = audioclip.duration
                audioclip.close()
            else:
                self.goodToUse = False

    def requestAudio(self) -> bool:
        try:
            # Request speech synthesis
            response = self.speechEngine.synthesize_speech(Text=self.com.body, OutputFormat="mp3", VoiceId="Brian")
        except (BotoCoreError, ClientError) as error:
            # The service returned an error
            print(error)
            return False

            # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(self.mp3Path)

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                        return True
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    return False
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            return False

    def populateChildComments(self):
        isStillGoodComments = True
        clickedContinueThread = False
        commentCount = 1
        compareScore = self.com.score
        child = self.com.replies[0]
        threadId = child.id

        if(type(child)==MoreComments): # I dont deal with this case for right now...
            isStillGoodComments = False

        while(isStillGoodComments):
            if(child.score/compareScore >= self.PERCENT_TO_BEAT and commentCount < self.MAX_CHILD_COMMENTS):
                if(len(child.body.split(" ")) < self.MAX_AMOUNT_OF_WORDS):

                    if(commentCount == 2):
                        try:
                            threadElm = WebDriverWait(self.drv, self.timeout).until(
                            lambda x: x.find_element(By.XPATH, f"//div[@id='continueThread-t1_{threadId}']/div[2]/a"))
                            
                            threadElm.click()
                        except TimeoutException:
                            isStillGoodComments = False
                            print("Page load timed out, could not continue the thread...")
                            break
                        else:
                            clickedContinueThread = True

                    redditChildComment = RedditComment(self.speechEngine, self.drv, child, self.identifier + str(commentCount))
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

    def resizeCommentImage(self):
        f1 = Image.open(self.pngPath)
        self.w, self.h = f1.size

        self.h = int(self.COMMENT_WIDTH/self.w*self.h)
        self.w = self.COMMENT_WIDTH

        #f1 = f1.resize((self.w, self.h), Image.ANTIALIAS)

        f1 = ImageOps.fit(f1, (self.w, self.h))

        return f1

    def buildVideoFrames(self):

        bgBase = Image.open(BACKGROUND_FILE_DIR)
        bgX, bgY = bgBase.size

        hOffset = (bgY-self.h)//8 # check
        
        totalCommentHeight = 0
        commentList = []
        commentImg = RedditCommentImage(self)
        commentList.append(commentImg)
        totalCommentHeight += commentImg.h
        for comment in self.childComments:
            commentImg = RedditCommentImage(comment)
            commentList.append(commentImg)
            totalCommentHeight += commentImg.h

        wOffset = (bgX-commentList[0].w)//2
        rescaleHeightFactor = (bgY - hOffset)/totalCommentHeight

        if(rescaleHeightFactor*commentList[0].w > bgX):
            rescaleHeightFactor = (bgX-wOffset)/commentList[0].w

        prevCommentH = hOffset
        for idx, comment in enumerate(commentList):
            f1 = comment.resizeCommentImage(rescaleHeightFactor)
            bgBase.paste(f1, ((bgX-comment.w)//2, hOffset))
            comment.redditComment.commentFrameDir = os.path.join(COMMENT_PNG_FRAME_DIR, f"f{str(idx+1)}_{self.getId()}.png")
            bgBase.save(os.path.join(COMMENT_PNG_FRAME_DIR, comment.redditComment.commentFrameDir))

            prevCommentH = comment.h
            hOffset += prevCommentH

    def getId(self):
        return self.com.id

    def getElmId(self):
        return f"t1_{self.com.id}"

