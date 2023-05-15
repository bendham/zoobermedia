from video.RedditVideoInterface import RedditVideoInterface
from video.Thumbnail import Thumbnail

if __name__ == "__main":
    # Require sub name, episode number, and how many thumbnails are required!
    thumbnails = 20
    sub = "contagiouslaungter"
    episode_num = 7

    # Get videos
    video_to_make_info = {"subreddit": "contagiouslaungter", "numberOfClips" : thumbnails, 'videoNumber': episode_num}
    video_finder = RedditVideoInterface(video_to_make_info)

    # Make thumbnails from them
    video_finder.generateThumbnailList()


    

