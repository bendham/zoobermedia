from pymongo import MongoClient
from video.secrets import mongo_string
from video.Helpers import *
import os

baseURL = "http://localhost:3000/api";

client: MongoClient = MongoClient(mongo_string)

db = client['zoobermedia']
data = db['datas'].find_one()

print(data)

# addDay(data)

# print(data)

# db['datas'].replace_one({'zooberType': 'main'}, data)

urlString = "http://localhost:3000/images/"

images = [f for f in os.listdir(THUMBNAIL_SAVE_DIR) if os.path.isfile(os.path.join(THUMBNAIL_SAVE_DIR, f))]

imList = []
if images:
    for im in images:
        imList.append(urlString + im)

    data['thumbnails'] = imList

updateDBData(data)

print(imList)

