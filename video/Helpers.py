from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import subprocess
import os
from settings import *
import json

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
    print(directory)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if len(exclude) >= 1:
        for exc in exclude:
            for file in files:
                if exc in file:
                    files.remove(file)

    for file in files:
        print(file)
        os.remove(os.path.join(directory, file))


def cleanUpFiles():
    deleteDirectory(THUMBNAIL_SAVE_DIR)
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



def updateVideoDeatils():

    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        videoDetails['content'][videoDetails['video']]['number'] = videoDetails['content'][videoDetails['video']]['number'] + 1

        vidFile.seek(0)
        vidFile.truncate()

        json.dump(videoDetails, vidFile, indent=1)

def isVideoSuccess():
    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        attempt = json.load(vidFile)['attempt']

    if attempt == 'success':
        return True
    else:
        return False

def setVideoToMake(update):
    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        videoDetails['video'] = update

        vidFile.seek(0)
        vidFile.truncate()

        json.dump(videoDetails, vidFile, indent=1)

def setAttemptTo(update):
    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        videoDetails['attempt'] = update

        vidFile.seek(0)
        vidFile.truncate()

        json.dump(videoDetails, vidFile, indent=1)

def readDay():
    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
           return json.load(vidFile)['day']

def addDay():
    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        videoDetails['day'] = (videoDetails['day'] + 1) % 7

        vidFile.seek(0)
        vidFile.truncate()

        json.dump(videoDetails, vidFile, indent=1)

def updateSubIds():
    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        listOfSubids = videoDetails['content']['redditcomment']['meta']
        oldSubids = videoDetails['content']['redditcomment']['old']

        if len(listOfSubids) >= 1:
            usableSubids = listOfSubids[0]
            oldSubids.append(usableSubids)

            videoDetails['content']['redditcomment']['meta'] = listOfSubids[1:]
            videoDetails['content']['redditcomment']['old'] = oldSubids

            vidFile.seek(0)
            vidFile.truncate()

            json.dump(videoDetails, vidFile, indent=1)

            return usableSubids
        else:
            return None

def getSubIds():
    with open(UPLOAD_INFO_FILE_DIR, 'r+') as vidFile:
        videoDetails = json.load(vidFile)
        listOfSubids = videoDetails['content']['redditcomment']['meta']
        if len(listOfSubids) >= 1:
            usableSubids = listOfSubids[0]
            return usableSubids
        else:
            return None