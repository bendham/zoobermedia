import os

CW_DIR = os.getcwd()

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
        

UPLOAD_INFO_FILE_DIR = os.path.join(CW_DIR, 'bin', 'upload_info.json')

YOUTUBE_API = os.path.join(CW_DIR, 'bin', 'youtubeAPI', 'video')

YOUTUBE_API_UPLOAD_DESC = os.path.join(YOUTUBE_API,"description")
YOUTUBE_API_UPLOAD_TAGS = os.path.join(YOUTUBE_API,"tags")
YOUTUBE_API_UPLOAD_TITLE = os.path.join(YOUTUBE_API,"title")