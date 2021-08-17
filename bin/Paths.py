import os


class Paths:

    def __init__(self):
        self.cwDir = os.getcwd()
        self.videoContentDir = os.path.join(self.cwDir, 'video', 'video-content')
        self.clipDir = os.path.join(self.videoContentDir,'clips')
        self.clipVideoDir = os.path.join(self.clipDir, "video")
        self.clipAudioDir = os.path.join(self.clipDir, "audio")
        self.finalDir = os.path.join(self.videoContentDir, 'final')
        self.zooberContentDir = os.path.join(self.videoContentDir, 'zoober-content')
        self.watermarkFileDir = os.path.join(self.zooberContentDir, 'watermark.png')
        

        self.uploadInfoFileDir = self.videoContentDir = os.path.join(self.cwDir, 'bin', 'upload_infor.json')