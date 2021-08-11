from video.Video import Video


class VideoHandler:


    def __init__(self):
        self.vidArray = []

    def addVid(self, video):

        self.vidArray.append(video)

    def removeVid(self, video):
        self.vidArray.remove(video)

