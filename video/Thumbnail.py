import random
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import json
import math

from settings import *

class Thumbnail:

    NUM_OF_THUMB = 5

    def __init__(self):
        self.FONT = "FRAHV.TTF"
        self.SIZE = (1280,720)
        self.thumbnailPathArray = []
        self.vidsForThumbnail = []

    def addThumbnailPath(self, possibleThumbnail):
        self.thumbnailPathArray = self.thumbnailPathArray.append(possibleThumbnail)

    def generateThumbnails(self, withWord=True, withFace=True):

        faceChoice = None                    
        if(withWord):
            with open(UPLOAD_INFO_FILE_DIR) as uploadInfo:
                currentVideoDetails = json.load(uploadInfo)['current-video']

            wordDir = os.path.join(THUMBNAIL_WORDS_DIR, currentVideoDetails['sub'])

            wordDetails = {'path':self.pickPath(wordDir),'number':currentVideoDetails['number']}

        if(withFace):
            faceChoice = self.pickPath(THUMBNAIL_FACES_DIR, wordDetails)

        
        for videoThumbnailDir in self.thumbnailPathArray:
            self.produceThumbnail(videoThumbnailDir, wordDetails, faceChoice)

            

    def produceThumbnail(self,dir, wordDetails=None, faceDir=None):

        # if(wordDetails):
        #     wordImage = Image.open(wordDetails['path'])
    
        # baseImg = Image.open(dir)
        # baseImg = baseImg.resize(self.SIZE,Image.ANTIALIAS)


        return


    
    def pickPath(self, path, wordDetails=None):
       
        if(wordDetails):
            side = 'left'
            if('right' in wordDetails['path']):
                side = 'right'

            files = os.listdir()
            chosenFile =  random.choice(files)
            while(side not in chosenFile):
                chosenFile =  random.choice(files)


            return chosenFile
        else:
            return random.choice(os.listdir(path)) 

    def checkCandidateForThumbnail(self, vidFileDir):
        numberOfThumbnails = len(self.thumbnailPathArray)

        if(numberOfThumbnails < self.NUM_OF_THUMB):
            vid =  VideoFileClip(vidFileDir)
            if vid.h * vid.w >= 720*1080:
                self.vidsForThumbnail.append(vidFileDir)
            vid.close()

    def getFinalThumbs(self, ADD_FACE, ADD_WORD):
        self.getThumbnail()
        self.generateThumbnails(ADD_FACE, ADD_WORD)

    def getThumbnail(self):

        for num, vidDir in enumerate(self.vidsForThumbnail):

            vid =  VideoFileClip(vidDir)
            
            if vid.h * vid.w >= 720*1080:

                intVidDuration = math.floor(vid.duration)
                
                lowEnd = math.floor(intVidDuration/4)
                hiEnd = math.floor(intVidDuration*3/4)

                thumbNailTime = random.randint(lowEnd, hiEnd)

                thumbnailFilePath = os.path.join(THUMBNAIL_SAVE_DIR, f"thumbnailChoice{num+1}.png")

                vid.save_frame(thumbnailFilePath, t=thumbNailTime)
                self.addThumbnailPath(thumbnailFilePath)

            vid.close()

        


