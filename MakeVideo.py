from video.RedditVideoInterface import RedditVideoInterface
from video.RedditCommentVideoInterface import RedditCommentVideoInterface
from settings import *
from video.Helpers import *
from bin.youtubeAPI.uploadFinal import uploadVideo
import sys, json

if __name__ == "__main__":

    print("Generating new compilation...\n")

    isScheduledVideo = True if len(sys.argv) < 2 else False

    if(not isScheduledVideo):
        # Probably a single video request
        video_to_make_info = json.loads(sys.argv[1].replace("'", '"'))
    else:
        # Regular schedule!

        video_creation_data = getDBData()

        current_day = readDay(video_creation_data)
        video_to_make_info = video_creation_data['videos'][current_day]

    if video_to_make_info['isMakingVideo']:
        # Will be making a video
        if video_to_make_info['iscomment']:
            # Comment Video
            new_video_interface = RedditCommentVideoInterface(video_to_make_info)

        else:
            # Normal video (does not include twitch videos)
            new_video_interface = RedditVideoInterface(video_to_make_info)

        # Clean thubnails, as now they are not needed with a new video being made
        deleteDirectory(THUMBNAIL_SAVE_DIR)


        # new_video_interface.generateVideoList()

        # For now, assume the video was a success
        try:
            # uploadVideo(video_to_make_info)

            if(isScheduledVideo):
                incrementEpisodeNumber(video_creation_data, video_to_make_info)
                addDay(video_creation_data)
                updateThumbnailArrayLinks(video_creation_data)


                updateDBData(video_creation_data)
            cleanUpFiles()

        except Exception as exp:
            print("Could not upload!")
            print(exp)
            cleanUpFiles()
    else:
        if(isScheduledVideo):
            video_creation_data = getDBData()
            addDay(video_creation_data)
            updateDBData(video_creation_data)
    
    
