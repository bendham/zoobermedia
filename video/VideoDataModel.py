from abc import ABCMeta
import array

class VideoModel(metaclass=ABCMeta):
    isMakingVideo: bool
    dayOfWeek: int
    iscomment: bool
    subreddit: str
    numberOfClips: int
    videoNumber: int
    title: str
    descrption: str
    commentSubreddits: array
    clipsPerSub: int
    thumbnails: array
