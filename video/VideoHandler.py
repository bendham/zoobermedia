from logging import getLogRecordFactory
import math
import subprocess

from moviepy.video.VideoClip import VideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
from video.Thumbnail import Thumbnail
import requests
import os
from moviepy import *
from settings import *

class VideoHandler:

    def __init__(self):
        self.vidArray = []
        self.thumbnail = Thumbnail()

    def addVid(self, video):

        self.vidArray.append(video)

    def removeVid(self, video):
        self.vidArray.remove(video)
    
    def writeContentFromRequest(self, req, vidDir):
        with open(vidDir, "wb" ) as media:
            media.write(req.content)

    def urlRequest(self, url):
        return requests.get(url)

    def removeFile(self, fileDirArray):
            for fileDir in fileDirArray:
                if(fileDir not in self.thumbnail.vidsForThumbnail):
                    os.remove(fileDir)
    
    def getThumbnail(self, ADD_FACE, ADD_WORDS):
        self.thumbnail.getFinalThumbs(ADD_FACE, ADD_WORDS)
        self.thumbnail.cleanUpThumbnailVideos()

    def concat(self):
        vidList = list(map( lambda vid : os.path.join(CLIP_DIR ,vid), os.listdir(CLIP_DIR)[2:]))

        moviePyVids = []
    
        for vidDir in vidList:
            moviePyVids.append(VideoFileClip(vidDir))
        
        moviePyVids.append(VideoFileClip(ZOOBER_OUTRO))
        
        finClip = concatenate_videoclips(moviePyVids, method='compose')
        finClip.write_videofile(FINAL_SAVE)
        
        # Close and get rid of last item (the outro)
        moviePyVids[-1].reader.close()
        moviePyVids = moviePyVids[:-1]

        # Close and get rid of all videos
        for idx, video in enumerate(moviePyVids):
            video.reader.close()
            os.remove(vidList[idx])

    def concatVidList(self, vidList, saveLocation, hasOutro=False):
        moviePyVids = []
    
        for vid in vidList:
            moviePyVids.append(VideoFileClip(vid.finalSave))
            # if(vid != vidList[-1]):
            #     moviePyVids.append(VideoFileClip(CUT_FILE_DIR))
        
        finClip = concatenate_videoclips(moviePyVids, method='compose')
        finClip.write_videofile(saveLocation)
        if(hasOutro):
            # Close and get rid of last item (the outro)
            moviePyVids[-1].reader.close()
            moviePyVids = moviePyVids[:-1]
            vidList = vidList[:-1]

        # Close and get rid of all videos
        for video in moviePyVids:
            video.reader.close()
            
        for idx, video in enumerate(vidList):   
            os.remove(vidList[idx].finalSave)

    def concatFFmpeg(self, textDir):
        textFileDir = textDir.replace("\\", "/")
        subprocess.call(f"ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i {textFileDir} -c copy {FINAL_SAVE}", shell=True)

        #os.remove(textDir)
    