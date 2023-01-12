from video.RedditVideoInterface import RedditVideoInterface
from video.RedditCommentVideoInterface import RedditCommentVideoInterface
from settings import *
from video.Helpers import *
from bin.youtubeAPI.uploadFinal import uploadVideo

if __name__ == "__main__":

    print("Generating new compilation...\n")

    video_creation_data = getDBData()

    current_day = readDay(video_creation_data)
    video_to_make_info = video_creation_data['videos'][current_day]

    if video_to_make_info['isMakingVideo']:
        # Will be making a video
        if video_to_make_info['iscomment']:
            # Comment Video
            new_video_interface = RedditCommentVideoInterface(video_to_make_info['subreddit'], video_to_make_info['commentSubreddits'])

        else:
            # Normal video (does not include twitch videos)
            new_video_interface = RedditVideoInterface(video_to_make_info['subreddit'], video_to_make_info['numberOfClips'])

        cleanUpFiles()
        new_video_interface.generateVideoList()

        # For now, assume the video was a success
        try:
            uploadVideo()

            incrementEpisodeNumber(video_to_make_info)
            video_creation_data['videos'][current_day] = video_to_make_info
            addDay(video_creation_data)
            updateThumbnailArrayLinks(video_creation_data)


            updateDBData(video_creation_data)
        except(Exception):
            print("Could not upload!")
    
    
