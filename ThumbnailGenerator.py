from settings import THUMBNAIL_SAVE_DIR
from video.RedditVideoInterface import RedditVideoInterface
from video.Thumbnail import Thumbnail
from video.Helpers import cleanUpFiles, deleteDirectory



import json
import sys

if __name__ == "__main__":
    print("Starting!")
    cleanUpFiles()

    # Clean thubnails, as now they are not needed with a new video being made
    deleteDirectory(THUMBNAIL_SAVE_DIR)

    # Require sub name, episode number, and how many thumbnails are required!
    # video_to_make_info = json.loads(sys.argv[1].replace("'", '"'))

    # Get videos
    video_to_make_info = {"subreddit": "contagiouslaughter", "numberOfClips" : 10, 'videoNumber': 2}
    video_finder = RedditVideoInterface(video_to_make_info)

    # Make thumbnails from them
    print("Making thumbanils")
    video_finder.generateThumbnailList()

    cleanUpFiles()
