# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 21:05:20 2019

@author: bendh
"""

from dotenv import load_dotenv
load_dotenv()

import ffmpeg_normalize
import praw
import json
import requests
from bs4 import BeautifulSoup
import urllib.request
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
import ffmpeg
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
import subprocess
import ast

SITE_URL = "https://www.reddit.com"

def videoURL(rr,subreddit,num,episodeNum):
    
    print(f"This is the episode number {episodeNum}")

    redditVideoList = []
    dumbyList = []
    redditVideoURL = "v.redd.it"

    sub = rr.subreddit(subreddit)

    for submission in (sub.hot(limit=int(num)) if int(episodeNum) != 50 else sub.top(time_filter='year', limit=50)):#do a map
    
        submissionURL = submission.url
        dumbyList.append(submissionURL)

        if redditVideoURL in submissionURL:
            directLink = submission.permalink
            redditVideoList.append(SITE_URL+directLink)#needs to be special so the json file can be added

    if int(episodeNum) == 50: #If it's the speacial '50th' video add all of this time arounds posts to the end of the list after the yearly top posts
        for submission in sub.hot(limit=int(num)):
            submissionURL = submission.url

            dumbyList.append(submissionURL)

            if redditVideoURL in submissionURL:
                directLink = submission.permalink
                redditVideoList.append(SITE_URL+directLink)

    print(f"Dumbylist: {dumbyList}")
    print(f"Length: {len(dumbyList)}")

    print(redditVideoList)
    print(f"There are {len(redditVideoList)} posts collected")

    return redditVideoList
    
def jsonLinks(linkList):
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    videoList = []
    audioList = []
    
    for url in linkList:

        jsonUrl = url[:-1] + ".json"
        json_data = requests.get(jsonUrl, headers=headers).json()
        jsonDataChop = json_data[0]["data"]["children"][0]["data"]#chops the json file down to a point where some keys beyond this point might be differnet
        
        if json_data[0]["data"] == 'nsfw':
            print("NSFW post...")
            continue
        if "crosspost_parent_list" in jsonDataChop.keys(): #seperates the cross posted post with the non-one. Does the same thing but they are located in different spots
            #if jsonDataChop["secure_media"] == None:
            #    continue
            #
            #There was a time where on isntantkarma subreddit, there was a corssposted post, but the link
            #could not be accessed as the subreddit was private. Thus a fix needs to be done if it happens agian
            #Suggestion:Check if the crosspost_parent_list has None in the respective json file
            try:
                #jsonDataChop["crosspost_parent_list"][0]["secure_media"]
                videoLink = jsonDataChop["crosspost_parent_list"][0]["secure_media"]["reddit_video"]["fallback_url"]
            except:
                print("Not compatable")
            
            #videoLink = jsonDataChop["crosspost_parent_list"][0]["secure_media"]["reddit_video"]["fallback_url"]
        else:
            #if jsonDataChop["secure_media"] == None:
            #    continue
            try:
                videoLink = jsonDataChop["secure_media"]["reddit_video"]["fallback_url"]
            except:
                print("Not compatable...")

        positionOfDash = videoLink.find('DASH')#finds where dash is in the medialink
        audioLink = videoLink[:positionOfDash]+"DASH_audio.mp4"#converts the link to an aduio link by replacing dash
        
        videoList.append(videoLink)
        audioList.append(audioLink)
        
    return [videoList,audioList]

def download(direc,urlList,markLocation):
    print('This is the direc: %s'%direc)
    print('This is the urlList:%s'%urlList)
    frameSize = 0
    thumbClip = ""
    num = 0
        
    finList = []
    removeList = []
    load_dotenv()
    ffmpeg_dir = os.getenv("FFMPEG_DIR")
    for idx,url in enumerate(urlList[0]):#starts iterating through the video links
        num+=1
        stringNum = str(num)

        videoReq = requests.get(url)
        audioReq = requests.get(urlList[1][idx])
        
        ID_DIR = os.path.join(direc,"VID%s.mp4"%stringNum)

        videoLocation = os.path.join(direc,"VID%s.mp4"%stringNum)
        audioLocation = os.path.join(direc,"AUD%s.mp3"%stringNum)
        
        
        with open(videoLocation, "wb" ) as video:
            video.write(videoReq.content)
                
        with open(audioLocation, "wb" ) as audio:
            audio.write(audioReq.content)
        
        sizeVideo = os.stat(videoLocation).st_size
        sizeAudio = os.stat(audioLocation).st_size
        
        print("This is size of video: " + str(sizeVideo))
        
        if sizeVideo > 1000 and sizeAudio > 1000  and sizeVideo < 2.5*(10**7):
            saveLocation = os.path.join(direc,"VIDAUD%s.mp4"%stringNum)

            normaudioLocation = os.path.join(direc,"AUDN%s.wav"%stringNum)
            print('ffmpeg-normalize {} -o {}'.format(audioLocation,normaudioLocation))
            commandOne = 'ffmpeg-normalize {} -o {}'.format(audioLocation,normaudioLocation)
            subprocess.call(commandOne,shell=True)

            commandTwo = '{} -i {} -i {} -i {} -filter_complex "[0]scale=1280:720,setsar=1:1,boxblur=10[bg];[0]scale=-1:720,setsar=16:9[main];[bg][main]overlay=(W-w)/2:(H-h)/2[markit];[markit][2] overlay" {}'.format(ffmpeg_dir,videoLocation,normaudioLocation,markLocation,saveLocation)
            subprocess.call(commandTwo,shell=True)


            videoClip = VideoFileClip(videoLocation)

            """
            videoClipResize = videoClip.resize(height=720, width=1080)
            videoClipResize.write_videofile(location, audio=audioLocation)
            """
            videoClip.reader.close()
            

            finList.append(saveLocation)
            testArea = videoClip.h * videoClip.w
            
            if  testArea > frameSize:
                frameSize =  testArea
                thumbClip = videoLocation
                vidDur = videoClip.duration

            os.remove(normaudioLocation)
        else:
            print("\nVideo could not process...\n")
        
        #os.remove(videoLocation) Not done hear becasue a thumbnail needs to be selected.
        removeList.append(videoLocation)
        os.remove(audioLocation)   
    """This for loop existed for the sake of making the thumbnail. 
    before the video is all deleted the biggest screen needs to be selected
    to make the thumbnail hd.
    """
    for direc in removeList:
        if direc is not thumbClip:
            os.remove(direc)

    return (finList,thumbClip,vidDur)#It is math.floor as the time is eaiset worked as an int

def concat(direcList,saveLocation):
    
    vidList = []
    
    for direc in direcList:
        vidList.append(VideoFileClip(direc))
    
    outroDir = os.path.join(saveLocation,"outro.mp4")
    vidList.append(VideoFileClip(outroDir))

    #Took out the add for the time being
    """
    audibleDir = os.path.join(saveLocation,"audible.mp4")
    vidList.insert(1,VideoFileClip(audibleDir))
    """
    
    finClip = concatenate_videoclips(vidList,method='compose')
    finClip.write_videofile(os.path.join(saveLocation,'funny_moments.mp4'))
    
    for video in vidList:
        video.reader.close()
    
    for direc in direcList:
        os.remove(direc)

def addWord(sub):
    
    wordsDir = os.getenv("WORD_THUMB_DIR")

    wordsAll = os.listdir(wordsDir)
    updateWordList = [i for i in wordsAll if sub in i]
    
    wordChoice = random.choice(updateWordList)

    if "right" in wordChoice:
        wordSide = "right"
    else:
        wordSide = "left"

    return (os.path.join(wordsDir,wordChoice),wordSide)

def thumb(saveDirec,videoDirec,time,sub,num,data):
    FONT = "FRAHV.TTF"
    SIZE = (1280,720)

    wordDirec,wordSide = addWord(sub)
    
    thumbDirec = os.path.join(saveDirec,"thumbnail.png")
    thumbEditDirec = os.path.join(saveDirec,"funny_moments.png")
    fontDirec = os.path.join(saveDirec,"thumbnail",FONT)

    
    timeInt = math.floor(time)
    thumbTime = random.randint(0,timeInt)+(random.randint(1,9)/10.0)
    
    videoThumb = VideoFileClip(videoDirec)
    videoThumb.save_frame(thumbDirec,t=thumbTime)
    videoThumb.close()    
    
    "Resize image at videoDirec, combine pngs on it...done"
    
    wordImage = Image.open(wordDirec)
    
    baseImg = Image.open(thumbDirec)
    baseImg = baseImg.resize(SIZE,Image.ANTIALIAS)

    baseImg.paste(wordImage,(0,0), wordImage)

    if wordSide == "left":
        x = 10
        y = 320
    else:
        x = 980
        y = 320

    b = 5

    font = ImageFont.truetype(fontDirec,130)

    numberWord = "#{}".format(num)

    d = ImageDraw.Draw(baseImg)

    d.text((x-b,y-b), numberWord, fill="black",font=font)
    d.text((x+b,y+b), numberWord, fill="black",font=font)
    d.text((x-b,y+b), numberWord, fill="black",font=font)
    d.text((x+b,y-b), numberWord, fill="black",font=font)

    d.text((x,y), numberWord, fill="white",font=font)

    baseImg.save(thumbEditDirec)
    
    os.remove(thumbDirec)
 
def uploadVideo(choice):
    if choice == "n":
        print("Video Succesfully downloaded...")
    else:
        os.system('python uploadVidV2.py')

def getVideoNum(sub,fileDirec):

    with open(fileDirec,"rt") as file:
        data = file.readline()

    lastVideoNum = data
    currentVideoNum = int(lastVideoNum) + 1

    with open(fileDirec,"wt") as file:
        file.writelines(str(currentVideoNum))

    return currentVideoNum

def main():

    SUB_PICK = "contagiouslaughter"
    UPLOAD= "y"
    SUB_AMOUNT = 60

    reddit = praw.Reddit(client_id='7EnZZe9pViFt7Q', client_secret='z7pn_Jsr0m1iagtaFyuCQpDoXtA', user_agent='my user agent')

    load_dotenv()

    fileDirectory = os.getenv("MAKE_VID_DIR")
    print("This is the file dir: %s" % fileDirectory)

    finalDir = os.path.join(fileDirectory, 'video')
    saveClipsDirec = os.path.join(fileDirectory, 'video', 'clips')
    markDir = os.path.join(fileDirectory,'video','watermark.png')

    clEpisodeDir = os.path.join(fileDirectory,"bin",'contagiousLaughterUploadCounter.txt')
    videoNumber = getVideoNum(SUB_PICK,clEpisodeDir)

    URLS = videoURL(reddit, SUB_PICK, SUB_AMOUNT, videoNumber)
    jsonURLS = jsonLinks(URLS)

    videoDirecs,thumbDirec,duration = download(saveClipsDirec,jsonURLS,markDir)
    thumb(finalDir,thumbDirec,duration,SUB_PICK,videoNumber,clEpisodeDir)
    os.remove(thumbDirec)
    concat(videoDirecs,finalDir)

    uploadVideo(UPLOAD)
    

    #print(duration)
    #print(thumbDirec)
    
    
main()