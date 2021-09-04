import random
from PIL import Image, ImageDraw, ImageFont
import os
import json

from settings import *

class Thumbnail:

    def __init__(self):
        self.FONT = "FRAHV.TTF"
        self.SIZE = (1280,720)
        self.thumbnailPathArray = []

    def addThumbnailPath(self, possibleThumbnail):
        self.thumbnailPathArray = self.thumbnailPathArray.append(possibleThumbnail)


    
    def generateThumbnails(self, withWord=True, withFace=True):

        wordChoice = None
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

            

    def produceThumbnail(dir, wordDetails=None, faceDir=None):

        


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


