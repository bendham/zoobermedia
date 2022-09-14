from video.RedditVideoInterface import RedditVideoInterface
from video.RedditCommentVideoInterface import RedditCommentVideoInterface
import os
import sys
from settings import *
from video.Helpers import *
from bin.youtubeAPI.uploadFinal import uploadVideo

if __name__ == "__main__":

    os.chdir(os.path.dirname(sys.argv[0]))

    print("Generating new compilation...\n")

    day = readDay()
    videoToMake = ""

    if day == 1 or day == 4: 
        videoToMake = "contagiouslaughter"
    elif day == 0 or day == 3:
        videoToMake = "watchpeopledieinside"
    elif day == 2:
        videoToMake = "redditcomment"
    else:
        videoToMake = "nothing"

    setVideoToMake(videoToMake)

    if videoToMake != "nothing":
        for i in range(0, 3):
            if not isVideoSuccess():
                print(f"Attempt {i}")
                cleanUpFiles()

                if videoToMake == "contagiouslaughter":
                    newCompilation = RedditVideoInterface("contagiouslaughter")
                elif videoToMake == "watchpeopledieinside":
                    newCompilation = RedditVideoInterface("watchpeopledieinside")
                elif videoToMake == "redditcomment":

                    subids = getSubIds()
                    newCompilation = RedditCommentVideoInterface(subids)
                else:
                    print("Couldnt find videoToMake!")
                    newCompilation = None
                
                if newCompilation:
                    print("Making new Compilation")
                    newCompilation.generateVideoList()

    if isVideoSuccess():
        if videoToMake == "contagiouslaughter":
            ""
        elif videoToMake == "watchpeopledieinside":
            ""
        else: # RedditCommentVideoInterface
            updateSubIds() 

        isUploadGood = uploadVideo()

        if isUploadGood:
            updateVideoDeatils()
            addDay()
            setAttemptTo('fail')
        else:
            print("Upload faild!")
    else:
        print("Video could not be made!")
    
    
    
