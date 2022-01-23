import os
from settings import *
class RedditVideo:
    def __init__(self, postUrl, vidNum):
        self.postUrl = postUrl
        self.jsonPostUrl = postUrl[:-1] + ".json"

        self.vidNum = vidNum

        self.videoName = f"video{vidNum}.mp4"
        self.audioName = f"audio{vidNum}.mp3"
        self.normalizedAudioName = f"normalized_audio{vidNum}.wav"

        self.combinedName = f"video_and_audio{vidNum}.mp4"

        self.videoFileDir =  os.path.join(CLIP_VIDEO_DIR , self.videoName)
        self.audioFileDir =  os.path.join(CLIP_AUDIO_DIR, self.audioName)
        self.normAudioFileDir = os.path.join(CLIP_AUDIO_DIR, self.normalizedAudioName)
        self.combinedFileDir = os.path.join(CLIP_DIR, self.combinedName)

    def setVideoAndAudioUrl(self, videoLink):
        self.setVideoUrl(videoLink)
        self.setAudioUrl(videoLink)

    def setVideoUrl(self, videoUrl):
        self.videoUrl = videoUrl.split("?")[0]

    def setAudioUrl(self, videoLink):

        # Finds where DASH is in the medialink
        positionOfDash = videoLink.find('DASH')

        # Converts the link to an aduio link by replacing DASH with DASH_audio
        self.audioUrl = videoLink[:positionOfDash]+"DASH_audio.mp4"
    