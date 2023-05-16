from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import subprocess
import os
from settings import *
import json
from pymongo import MongoClient
from video.secrets import mongo_string
from video.VideoDataModel import VideoModel


def getDBData():
    client: MongoClient = MongoClient(mongo_string)

    db = client['zoobermedia']
    print(db)
    return db['datas'].find_one()

def updateDBData(data):
    client: MongoClient = MongoClient(mongo_string)
    db = client['zoobermedia']
    db['datas'].replace_one({'zooberType': 'main'}, data)

def updateThumbnailArrayLinks(data):
    urlString = ZOOBER_API_URL+"/images/"

    images = [f for f in os.listdir(THUMBNAIL_SAVE_DIR) if os.path.isfile(os.path.join(THUMBNAIL_SAVE_DIR, f))]

    imList = []
    if images:
        for im in images:
            imList.append(urlString + im)

        data['thumbnails'] = imList
    else:
        data['thumbnails'] = [DEFAULT_THUMBNAIL_FOR_CLIENT, DEFAULT_THUMBNAIL_FOR_CLIENT, DEFAULT_THUMBNAIL_FOR_CLIENT]



def requestAudio(speechEngine, savePath, message, voice_to_use) -> bool:
        try:
            # Request speech synthesis
            response = speechEngine.synthesize_speech(Text=message, OutputFormat="mp3", VoiceId=voice_to_use)
        except (BotoCoreError, ClientError) as error:
            # The service returned an error
            print(error)
            return False

            # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    # Open a file for writing the output as a binary stream
                    with open(savePath, "wb") as file:
                        file.write(stream.read())
                        return True
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    return False
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            return False

def turnPictureIntoVideo(picDir, audDir, dur, saveDir):
    ffmpegCommand = f"ffmpeg -loop 1 -y -i {picDir} -i {audDir} -t {dur} {saveDir}"
    subprocess.call(ffmpegCommand, shell=True)

def deleteDirectory(directory, exclude=[]):
    # print(directory)

    if os.path.isdir(directory):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


        for exc in exclude:
            for file in files:
                if exc in file:
                    files.remove(file)

        for file in files:
            # print(file)
            try:
                os.remove(os.path.join(directory, file))
            except:
                print(f"Could not remove {os.path.join(directory, file)}...skipping")
    else:
        print(f"'{directory}' is not a valid directory to delete...skipping!")


def cleanUpFiles():
    print("Cleaning files...")

    deleteDirectory(FINAL_DIR)
    deleteDirectory(COMMENT_MP3_DIR, ["silent075"])
    deleteDirectory(COMMENT_FINAL_VIDEO_DIR)
    deleteDirectory(COMMENT_FINAL_AUDIO_DIR)
    deleteDirectory(COMMENT_FINAL_DIR)
    deleteDirectory(COMMENT_PNG_DIR)
    deleteDirectory(COMMENT_PNG_FRAME_DIR)

    deleteDirectory(CLIP_DIR)
    deleteDirectory(CLIP_VIDEO_DIR)
    deleteDirectory(CLIP_AUDIO_DIR)


def incrementEpisodeNumber(video_db, video: VideoModel):
    for vid, idx in enumerate(video_db['videos']):
        if vid['subreddit'] == video['subreddit']:
            video_db['videos'][idx]['videoNumber'] += 1

    

def readDay(video_data):
    return video_data['currentDay']

def addDay(video_data):
    if video_data['currentDay'] == 6:
        video_data['currentDay'] = 0
    else:
        video_data['currentDay'] += 1


