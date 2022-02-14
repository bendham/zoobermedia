from ntpath import join
import os

GECKO_DIR = r"C:\Users\bendh\geckodriver-v0.30.0-win64\geckodriver.exe"

CW_DIR = os.getcwd()
BIN_DIR = os.path.join(os.getcwd(), "bin")

VIDEO_CONTENT_DIR = os.path.join(CW_DIR, 'video', 'video-content')
CLIP_DIR = os.path.join(VIDEO_CONTENT_DIR,'clips')
CLIP_VIDEO_DIR = os.path.join(CLIP_DIR, "video")
CLIP_AUDIO_DIR = os.path.join(CLIP_DIR, "audio")
FINAL_DIR = os.path.join(VIDEO_CONTENT_DIR, 'final')
FINAL_SAVE = os.path.join(FINAL_DIR, "funny_moments.mp4")

THUMBNAIL_DIR = os.path.join(VIDEO_CONTENT_DIR, "thumbnail")
THUMBNAIL_SAVE_DIR = os.path.join(THUMBNAIL_DIR, "prelim-thumbnail")
THUMBNAIL_WORDS_DIR = os.path.join(THUMBNAIL_DIR, "word")
THUMBNAIL_FACES_DIR = os.path.join(THUMBNAIL_DIR, "face")

ZOOBER_CONTENT_DIR = os.path.join(VIDEO_CONTENT_DIR, 'zoober-content')
ZOOBER_OUTRO = os.path.join(ZOOBER_CONTENT_DIR, "outro.mp4")
WATERMARK_FILE_DIR = os.path.join(ZOOBER_CONTENT_DIR, 'watermark.png')

UPLOAD_INFO_FILE_DIR = os.path.join(BIN_DIR, 'upload_info.json')

YOUTUBE_API = os.path.join(BIN_DIR, 'youtubeAPI', 'video')

YOUTUBE_API_UPLOAD_DESC = os.path.join(YOUTUBE_API,"description")
YOUTUBE_API_UPLOAD_TAGS = os.path.join(YOUTUBE_API,"tags")
YOUTUBE_API_UPLOAD_TITLE = os.path.join(YOUTUBE_API,"title")


# Mainly used for Reddit Comment Reading

REDDIT_COMMENT_READING_DIR = os.path.join(BIN_DIR, "reddit_comment_reading")

COMMENT_PNG_DIR = os.path.join(REDDIT_COMMENT_READING_DIR, "comment_png")
COMMENT_PNG_FRAME_DIR = os.path.join(COMMENT_PNG_DIR, "frames")
COMMENT_MP3_DIR = os.path.join(REDDIT_COMMENT_READING_DIR, "comment_mp3")
COMMENT_MP4_DIR = os.path.join(REDDIT_COMMENT_READING_DIR, "comment_mp4")
COMMENT_FINAL_VIDEO_DIR = os.path.join(COMMENT_MP4_DIR, "final_video")
COMMENT_FINAL_AUDIO_DIR = os.path.join(COMMENT_MP4_DIR, "final_audio")
COMMENT_FINAL_DIR = os.path.join(COMMENT_MP4_DIR, "final")
CONCAT_VID_LIST_FILE = os.path.join(COMMENT_FINAL_VIDEO_DIR, "concat.txt")


RESOURCES_DIR = os.path.join(REDDIT_COMMENT_READING_DIR, "resources")
BACKGROUND_FILE_DIR = os.path.join(RESOURCES_DIR, "blank.png")
SILENCE_FILE_DIR = os.path.join(RESOURCES_DIR, "silent075.mp3")
CUT_FILE_DIR = os.path.join(RESOURCES_DIR, "cut75fps.mp4")
FONT_FILE_DIR = os.path,join(RESOURCES_DIR, "Anson-Regular.otf")
