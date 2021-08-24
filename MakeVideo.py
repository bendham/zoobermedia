import json
from bin.Paths import Paths
from video.RedditVideoInterface import RedditVideoInterface



def updateVideoDeatils():
    paths = Paths()

    with open(paths.uploadInfoFileDir, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        videoDetails['current-video']['number'] = videoDetails['current-video']['number'] + 1

        vidFile.seek(0)
        vidFile.truncate()

        json.dump(videoDetails, vidFile, indent=1)

if __name__ == "__main__":

    print("Generating new compilation...\n")

    updateVideoDeatils()

    newCompilation = RedditVideoInterface("contagiouslaughter")
    newCompilation.generateVideoList()
