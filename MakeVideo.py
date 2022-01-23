import json
from video.RedditVideoInterface import RedditVideoInterface
from video.RedditCommentVideoInterface import RedditCommentVideoInterface

from settings import *

def updateVideoDeatils():

    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        videoDetails['current-video']['number'] = videoDetails['current-video']['number'] + 1

        vidFile.seek(0)
        vidFile.truncate()

        json.dump(videoDetails, vidFile, indent=1)

if __name__ == "__main__":

    print("Generating new compilation...\n")

    #updateVideoDeatils()

    newCompilation = RedditCommentVideoInterface()
    newCompilation.generateVideoList()
