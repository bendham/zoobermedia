import random
from bin.Paths import Paths
from PIL import Image, ImageDraw, ImageFont
import os
import json


class Thumbnail:

    def __init__(self):
        self.FONT = "FRAHV.TTF"
        self.SIZE = (1280,720)

        self.paths = Paths()



        self.thumbnailPathArray = []

    def addThumbnailPath(self, possibleThumbnail):
        self.thumbnailPathArray = self.thumbnailPathArray.append(possibleThumbnail)


    
    def generateThumbnails(self, withWord=True, withFace=True):

        wordChoice = None
        faceChoice = None
        
            
        if(withWord):
            with open(self.paths.uploadInfoFileDir) as uploadInfo:
                currentVideoDetails = json.load(uploadInfo)['current-video']

            wordDir = os.path.join(self.paths.thumbnailWords, currentVideoDetails['sub'])

            wordDetails = {'path':self.pickPath(wordDir),'number':currentVideoDetails['number']}

        if(withFace):
            faceChoice = self.pickPath(self.paths.thumbnailFaces, wordDetails)

        
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


