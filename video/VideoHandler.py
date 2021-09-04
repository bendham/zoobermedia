from logging import getLogRecordFactory
import math

from moviepy.video.VideoClip import VideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from video.Video import Video
from video.Thumbnail import Thumbnail
import requests
import os
from moviepy import *
import subprocess
import random

from settings import *

class VideoHandler:


    def __init__(self):
        self.vidArray = []
        self.thumbnail = Thumbnail()

    def addVid(self, video):

        self.vidArray.append(video)

    def removeVid(self, video):
        self.vidArray.remove(video)

    def processVideos(self):
    
        for vid in self.vidArray:
            vidFileDir =  os.path.join(CLIP_VIDEO_DIR , vid.videoName)
            audioFileDir =  os.path.join(CLIP_AUDIO_DIR, vid.audioName)
            normAudioFileDir = os.path.join(CLIP_AUDIO_DIR, vid.normalizedAudioName)

            self.downloadVid(vid, vidFileDir, audioFileDir)
            self.processVid(vid, vidFileDir, audioFileDir, normAudioFileDir)
            self.removeFile([vidFileDir, audioFileDir, normAudioFileDir])

    def downloadVid(self, vid, vidFileDir, audioFileDir):
        print(f"Downloading video #{vid.vidNum}...\n")
        
        videoReq = self.urlRequest(vid.videoUrl)
        self.writeContentFromRequest(videoReq, vidFileDir)

        auddioReq = self.urlRequest(vid.audioUrl)
        self.writeContentFromRequest(auddioReq, audioFileDir)

        #print(auddioReq.headers)

    def processVid(self, vid, videoFileDir, audioFileDir, normAudioFileDir):
        print(f"Processing video #{vid.vidNum}...\n")
        combinedFileDir = os.path.join(CLIP_DIR, vid.combinedName)

        self.checkCandidateForThumbnail(videoFileDir)

        # Normalize Audio
        subprocess.call(f'ffmpeg-normalize {audioFileDir} -o {normAudioFileDir}', shell=True)

        # Combine Video and Audio, and add a blurred background
        subprocess.call(f'ffmpeg -i {videoFileDir} -i {normAudioFileDir} -i {WATERMARK_FILE_DIR} -filter_complex "[0]scale=1280:720,setsar=1:1,boxblur=10[bg];[0]scale=-1:720,setsar=16:9[main];[bg][main]overlay=(W-w)/2:(H-h)/2[markit];[markit][2] overlay" {combinedFileDir}', shell=True)
    
    def writeContentFromRequest(self, req, dir):
        with open(dir, "wb" ) as video:
            video.write(req.content)

    def urlRequest(self, url):
        return requests.get(url)

    def removeFile(self, fileDirArray):
        if(fileDirArray not in self.thumbnail.thumbnailPathArray):
            for fileDir in fileDirArray:
                os.remove(fileDir)

    def checkCandidateForThumbnail(self, vidFileDir):
        numberOfThumbnails = len(self.thumbnail.thumbnailPathArray)

        if(numberOfThumbnails < 2):

            with open(vidFileDir, "wb") as vid:
                vid =  VideoFileClip(vidFileDir)
            

            if vid.h * vid.w > 720*1080:
                self.thumbnail.thumbnailPathArray.append(vidFileDir)

            intVidDuration = math.floor(vid.duration)
            
            lowEnd = math.floor(intVidDuration/4)
            hiEnd = math.floor(intVidDuration*3/4)

            thumbNailTime = random.randint(lowEnd, hiEnd)

            thumbnailFilePath = os.path.join(THUMBNAIL_SAVE_DIR, f"thumbnailChoice{numberOfThumbnails+1}")

            vid.save_frame(thumbnailFilePath, t=thumbNailTime)
            self.thumbnail.addThumbnailPath(thumbnailFilePath)

            vid.close()