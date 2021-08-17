from logging import getLogRecordFactory
from video.Video import Video
from bin.Paths import Paths
import requests
import os
import moviepy
import subprocess

class VideoHandler:


    def __init__(self):
        self.vidArray = []
        self.paths = Paths()

    def addVid(self, video):

        self.vidArray.append(video)

    def removeVid(self, video):
        self.vidArray.remove(video)

    def processVideos(self):
        videoDir = self.paths.clipVideoDir
        audioDir = self.paths.clipAudioDir

        for vid in self.vidArray:
            vidFileDir =  os.path.join(videoDir , vid.videoName)
            audioFileDir =  os.path.join(audioDir, vid.audioName)
            normAudioFileDir = os.path.join(audioDir, vid.normalizedAudioName)

            self.downloadVid(vid, vidFileDir, audioFileDir)
            self.processVid(vid, vidFileDir, audioDir, audioFileDir, normAudioFileDir)
            self.removeFile([vidFileDir, audioFileDir, normAudioFileDir])

    def downloadVid(self, vid, vidFileDir, audioFileDir):
        print(f"Downloading video #{vid.vidNum}...\n")
        
        videoReq = self.urlRequest(vid.videoUrl)
        self.writeContentFromRequest(videoReq, vidFileDir)

        auddioReq = self.urlRequest(vid.audioUrl)
        self.writeContentFromRequest(auddioReq, audioFileDir)

        #print(auddioReq.headers)

    def processVid(self, vid, videoFileDir, audioDir, audioFileDir, normAudioFileDir):
        print(f"Processing video #{vid.vidNum}...\n")
        combinedFileDir = os.path.join(self.paths.clipDir, vid.combinedName)

        # Normalize Audio
        subprocess.call(f'ffmpeg-normalize {audioFileDir} -o {normAudioFileDir}', shell=True)

        # Combine Video and Audio, and add a blurred background
        subprocess.call(f'ffmpeg -i {videoFileDir} -i {normAudioFileDir} -i {self.paths.watermarkFileDir} -filter_complex "[0]scale=1280:720,setsar=1:1,boxblur=10[bg];[0]scale=-1:720,setsar=16:9[main];[bg][main]overlay=(W-w)/2:(H-h)/2[markit];[markit][2] overlay" {combinedFileDir}', shell=True)
    
    def writeContentFromRequest(self, req, dir):
        with open(dir, "wb" ) as video:
            video.write(req.content)

    def urlRequest(self, url):
        return requests.get(url)

    def removeFile(self, fileDirArray):
        for fileDir in fileDirArray:
            os.remove(fileDir)
