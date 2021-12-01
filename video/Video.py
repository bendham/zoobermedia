class Video:
    def __init__(self, postUrl, vidNum):
        self.postUrl = postUrl
        self.jsonPostUrl = postUrl[:-1] + ".json"

        self.vidNum = vidNum

        self.videoName = f"video{vidNum}.mp4"
        self.audioName = f"audio{vidNum}.mp3"
        self.normalizedAudioName = f"normalized_audio{vidNum}.wav"

        self.combinedName = f"video_and_audio{vidNum}.mp4"

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
    