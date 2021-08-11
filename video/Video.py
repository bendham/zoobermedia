class Video:
    def __init__(self, postUrl, vidNum):
        self.postUrl = postUrl
        self.jsonPostUrl = postUrl[:-1] + ".json"

        self.vidNum = vidNum

    def setVideoAndAudioUrl(self, videoLink):
        self.setVideoUrl(videoLink)
        self.setAudioUrl(videoLink)

    def setVideoUrl(self, videoUrl):
        self.videoUrl = videoUrl

    def setAudioUrl(self, videoLink):

        # Finds where DASH is in the medialink
        positionOfDash = videoLink.find('DASH')

        # Converts the link to an aduio link by replacing DASH with DASH_audio
        self.audioUrl = videoLink[:positionOfDash]+"DASH_audio.mp4"
    