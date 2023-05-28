import random
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import json
import math

from settings import *

class Thumbnail:

    

    def __init__(self, subString, episodeNum, num_thumb=5):
        self.FONT = "FRAHV.TTF"
        self.SIZE = (1280,720)
        self.thumbnailPathArray = []
        self.vidsForThumbnail = []

        self.subString = subString
        self.episodeNum = episodeNum

        self.thumbnail_compare_size = 0
        self.num_thumb = num_thumb

    def addThumbnailPath(self, possibleThumbnail):
        self.thumbnailPathArray.append(possibleThumbnail)

    def cleanUpThumbnailVideos(self):
        for vidDir in self.vidsForThumbnail:
            os.remove(vidDir)

    def generateThumbnails(self, withWord=True, withFace=True):

        faceChoice = None    
        wordDetails = None

        for idx,videoThumbnailDir in enumerate(self.thumbnailPathArray):
            if(withWord):

                wordDir = os.path.join(THUMBNAIL_WORDS_DIR, self.subString)

                wordDetails = {'choice':self.pickPath(wordDir),'number': self.episodeNum}

            if(withFace):
                faceChoice = self.pickPath(THUMBNAIL_FACES_DIR, wordDetails)

            self.produceThumbnail(videoThumbnailDir, idx+1,wordDetails, faceChoice)

            

    def produceThumbnail(self, dir, numberThumb, wordDetails=None, faceDir=None):

        thumbSaveDirec = os.path.join(THUMBNAIL_SAVE_DIR,f"funnyMoments{numberThumb}.png")

        baseImg = Image.open(dir)
        baseImg = baseImg.resize(self.SIZE,Image.ANTIALIAS)

        if(faceDir):
            faceImage = Image.open(faceDir)
            baseImg.paste(faceImage,(0,0), faceImage)

        if(wordDetails):

            fontDir = ImageFont.truetype(os.path.join(THUMBNAIL_DIR, self.FONT), 130)
            b = 5
            x = 980
            y = 320

            wordImage = Image.open(wordDetails['choice'])

            baseImg.paste(wordImage,(0,0), wordImage)

            # Make number

            if "left" in wordDetails['choice']:
                x = 10
                y = 320

            numWord = "#{}".format(wordDetails['number'])

            d = ImageDraw.Draw(baseImg)

            d.text((x-b,y-b), numWord, fill="black",font=fontDir)
            d.text((x+b,y+b), numWord, fill="black",font=fontDir)
            d.text((x-b,y+b), numWord, fill="black",font=fontDir)
            d.text((x+b,y-b), numWord, fill="black",font=fontDir)

            d.text((x,y), numWord, fill="white",font=fontDir)

        baseImg.save(thumbSaveDirec)

        os.remove(dir)



    def pickPath(self, path, wordDetails=None):
       
        if(wordDetails):
            side = 'left'
            if('right' in wordDetails['choice']):
                side = 'right'

            files = os.listdir(path)
            chosenFile =  random.choice(files)
            while(side in chosenFile):
                chosenFile =  random.choice(files)


            return os.path.join(path, chosenFile)
        else:
            return os.path.join(path,random.choice(os.listdir(path)))

    def checkCandidateForThumbnail(self, vidFileDir):
        numberOfThumbnails = len(self.thumbnailPathArray)

        if(numberOfThumbnails < self.num_thumb):
            vid =  VideoFileClip(vidFileDir)
            if vid.h * vid.w >= 720*480:
                self.vidsForThumbnail.append(vidFileDir)
            vid.close()

    def getFinalThumbs(self, ADD_FACE, ADD_WORD):
        self.getThumbnail()
        self.generateThumbnails(ADD_FACE, ADD_WORD)

    def getThumbnail(self):

        for num, vidDir in enumerate(self.vidsForThumbnail):

            vid =  VideoFileClip(vidDir)
            
            if vid.h * vid.w >= 720*480:

                intVidDuration = math.floor(vid.duration)
                
                lowEnd = math.floor(intVidDuration/4)
                hiEnd = math.floor(intVidDuration*3/4)

                thumbNailTime = random.randint(lowEnd, hiEnd)

                thumbnailFilePath = os.path.join(THUMBNAIL_SAVE_DIR, f"thumbnailChoice{num+1}.png")

                vid.save_frame(thumbnailFilePath, t=thumbNailTime)
                self.addThumbnailPath(thumbnailFilePath)

            vid.close()

        


