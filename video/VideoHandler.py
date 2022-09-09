from logging import getLogRecordFactory
import math
from pickle import TRUE
import subprocess
from matplotlib.pyplot import prism

from moviepy.video.VideoClip import VideoClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
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

    def clean_up(self):
        for vid in self.vidArray:
            os.remove(vid.finalSave)

    def concat(self):
        vidList = [os.path.join(CLIP_DIR, vid) for vid in os.listdir(CLIP_DIR) if os.path.isfile(os.path.join(CLIP_DIR, vid))]
        # vidList = list(map( lambda vid : os.path.join(CLIP_DIR ,vid), os.listdir(CLIP_DIR)[2:]))

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
            moviePyVids.append(VideoFileClip(vid.finalSave, has_mask=True))
            # if(vid != vidList[-1]):
            #     moviePyVids.append(VideoFileClip(CUT_FILE_DIR))
        
        finClip = concatenate_videoclips(moviePyVids, method='compose', bg_color=None)

        if(hasOutro): # Dumb code -> this only runs when outro is active...
            finClip = CompositeVideoClip([VideoFileClip(BACKGROUND_VIDEO),finClip])

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

    def concatFFmpeg(self, concat_file, saveLocation):
        print("Making concat vid..")
        textFileDir = concat_file.replace("\\", "/")
        subprocess.call(f"ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i {textFileDir} -c copy {saveLocation}", shell=True)
        os.remove(concat_file)

    def addBackground(self, new_file_path, new_save):
        subprocess.call(f'ffmpeg -hide_banner -stream_loop -1 -i {BACKGROUND_VIDEO} -c:v libvpx-vp9 -i {new_file_path} -i {ZOOBER_OUTRO} -i {BACKGROUND_MUSIC} -filter_complex "[1:a][3:a]amix=inputs=2:duration=first[audOut];[1:v] [audOut] [2:v] [2:a] concat=n=2:v=1:a=1 [vTemp] [a];[0:v][vTemp]overlay=shortest=1[v]" -map "[v]" -map "[a]" {new_save}', shell=True)
    