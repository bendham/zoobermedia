from video.RedditComment import RedditComment
import subprocess
import os
import yake
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from praw.reddit import Submission
from settings import *
import sys
from video.VideoHandler import VideoHandler
from PIL import Image, ImageOps, ImageFont, ImageDraw
from string import ascii_letters
import textwrap
from video.Helpers import requestAudio, turnPictureIntoVideo
from moviepy.editor import AudioFileClip
from bing_image_downloader import downloader



class RedditCommentSubVid:

    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    NUMBER_OF_SECTIONS = 10
    SILENCE_TIME = 0.75 # 0.75 s pause between comment reading

    def __init__(self, subId, pollySession, prawSession) -> None:
        
        self.kw_extrator = yake.KeywordExtractor(lan="en", top=1 )

        self.subId = subId
        self.finalSave = os.path.join(COMMENT_FINAL_DIR, f"subVid_{subId}.mp4")
        
        self.introVidAudioPath = os.path.join(COMMENT_PNG_DIR, self.subId + ".mp3")
        self.introVidPath = os.path.join(COMMENT_PNG_DIR, self.subId + ".mp4")
        self.introPngPath = os.path.join(COMMENT_PNG_DIR, self.subId + ".png")
        self.introVidDur = 0

        self.pollySession = pollySession
        self.prawSession = prawSession

        self.url = "https://www.reddit.com"
        self.vidUrlAppear = "v.redd.it"
        self.comments = []

        self.vidHandler = VideoHandler()
    
    def generateVideoList(self):
        subMis = self.prawSession.submission(id=self.subId)
        print(f"Generating Videos for {subMis.title}")

        self.cmtsUrl = "https://www.reddit.com" + subMis.permalink

        self.makeIntro(subMis)
        self.populateList(subMis)
        self.removeUnusable()
        self.makeVideos()

        print(f"Done generating videos for {subMis.title}!")

    def makeIntro(self, subMis):
        print(f"Making intro!")
        title = subMis.title

        query_string = self.kw_extrator.extract_keywords(title)[0][0]
        downloader.download(query_string, limit=1,  output_dir=SUB_BACKGROUND, adult_filter_off=False, force_replace=False, timeout=60, verbose=False, filter="photo")

        downloadDir = os.path.join(SUB_BACKGROUND, query_string)
        downloading = True
        while(downloading):
            dirList = os.listdir(downloadDir)
            if(len(dirList) > 0):
                downloading = False
                background = os.path.join(downloadDir, dirList[0])
        
        # Thanks 
        # https://www.alpharithms.com/fit-custom-font-wrapped-text-image-python-pillow-552321/
        # For the great code

        bgBase = Image.open(background)
        bgBase.convert("RGB")

        bgBase = bgBase.copy() # Fixes colour bug?
        bgBase = ImageOps.fit(bgBase, (1280, 720))

        

        font = ImageFont.truetype(font="Anson-Regular.otf", size=72)

        draw = ImageDraw.Draw(im=bgBase)

        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(bgBase.size[0] * .90 / avg_char_width)

        text = textwrap.fill(text=title, width=max_char_count)
        draw.text(xy=(bgBase.size[0]//2, bgBase.size[1]//2), text=text, font=font, fill=(255, 255, 255), anchor='mm', stroke_fill=(0, 0, 0), stroke_width=2)
        bgBase.save(self.introPngPath)

        goodAudio = requestAudio(self.pollySession, self.introVidAudioPath, title, "Joanna")
        if(goodAudio):
            audioclip = AudioFileClip(self.introVidAudioPath)
            self.introVidDur = audioclip.duration
            audioclip.close()
            turnPictureIntoVideo(self.introPngPath, self.introVidAudioPath, self.introVidDur, self.introVidPath)

            self.removeTempIntroThings()

        os.remove(background)
        os.rmdir(downloadDir)

    def removeTempIntroThings(self):
        os.remove(self.introPngPath)
        os.remove(self.introVidAudioPath)

    def populateList(self, subMis):

        drv = self.setUpRedditPage(subMis)

        for idx, comment in enumerate(subMis.comments[1:self.NUMBER_OF_SECTIONS]):
            cmt = RedditComment(self.pollySession, drv, comment, idx+1, self.cmtsUrl)

            if(len(comment.body.split(" ")) < cmt.MAX_AMOUNT_OF_WORDS): # Check for parent comment to be reasonable in length
                print("Generating details for comment clip!")
                cmt.populateChildComments()
                cmt.buildVideoFrames()

                if(cmt.goodToUse):
                    self.comments.append(cmt)

        drv.quit()

    def removeUnusable(self):
        "This processing is already done when making the comments, the goodToUse boolean"
        
    def makeVideos(self):
        print(f"Starting making the clips!")
        # Process audio
        self.processAudio()
        # Process video and get rid of temp files
        self.processVideoAndCleanUp()
        # Cleanup
        self.cleanUp()
        # Combine in one
        self.concat()

    def cleanUp(self):
        for comment in self.comments:
            self.cleanupCommentFiles(comment)

    def processAudio(self):
        for comment in self.comments:
            duration = 0
            if(comment.goodToUse == True): # Add case for no child
                concatFileDir = comment.concatFileDir.replace("\\", "/") # Bug in FFMPEG where \ is not good for input file
                with open(concatFileDir, 'w') as f:
                    f.write(f"file '{comment.name}.mp3'\n")
                    duration += comment.dur
                    for child in comment.childComments:
                        f.write(f"file 'silent075.mp3'\n")
                        f.write(f"file '{child.name}.mp3'\n")
                        duration += child.dur + self.SILENCE_TIME
                
                    f.write(f"file 'silent075.mp3'\n")
                    duration += self.SILENCE_TIME
                comment.totalVidDuration = duration

            subprocess.call(f'ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i {concatFileDir} -t {duration} -c copy {comment.concatAudioFilePath}', shell=True)

    def processVideoAndCleanUp(self):
        for comment in self.comments:
            if(len(comment.childComments)==0):
                ffmpegCommand = f"ffmpeg -hide_banner -loglevel error -loop 1 -y -i {comment.commentFrameDir} -i {comment.concatAudioFilePath} -t {comment.totalVidDuration} {comment.finalSave}"
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

                ffmpegCommand = f'ffmpeg -hide_banner -loglevel error -loop 1 -y {inputString} -i {comment.concatAudioFilePath} -filter_complex "{filterString}" -t {comment.totalVidDuration} {comment.finalSave}'

            subprocess.call(ffmpegCommand, shell=True)

            self.vidHandler.addVid(comment.finalSave)

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

    def buildConcatList(self):
        vidList = []
        for comment in self.comments:
            vidList.append(comment.finalSave)
            if(comment != self.comments[-1]):
                vidList.append(CUT_FILE_DIR)
        return vidList
    
    def buildConcatText(self):
        with open(CONCAT_VID_LIST_FILE, 'w') as f:
            for comment in self.comments:
                f.write(f"file '{comment.name}.mp4'\n")
                if(comment != self.comments[-1]):
                    f.write(f"file cut75fps.mp4\n")

    def concat(self):

        self.vidHandler.concatVidList(self.comments, self.finalSave)

    def setUpRedditPage(self, subMission: Submission):

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.set_preference("dom.push.enabled", False)  # kill notification popup
        ser = Service(GECKO_DIR)
        drv = Firefox(options=opts, service=ser)
        drv.execute_script("document.body.style.zoom='250%'")
    
        drv.get(self.cmtsUrl)
        wait = WebDriverWait(drv, 10)
        try:
            profile_btn = wait.until(EC.presence_of_element_located((By.ID, "USER_DROPDOWN_ID"))) 
            profile_btn.click()

            nightModeThere = False

            try:
                night_mode_btn = drv.find_element(By.XPATH, "//div[@role='menu']/button")
                night_mode_btn.click()
                nightModeThere = True
            except:
                "Do nothing"
            
            if not nightModeThere:
                settings_button = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@role='menu']/div/button)[3]")))
                settings_button.click()

                night_mode_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@role='menu']/div/div)[3]/button")))
                night_mode_btn.click()
                
        except:
            print("Reddit could not be accessed properly. Quiting...")
            sys.exit()

        return drv

    