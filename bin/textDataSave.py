import ast

with open("data.txt","rt") as file:
    data = file.readlines()

srtDictionary = data[-1].strip().split(",",1)[1]
dataDict = ast.literal_eval(srtDictionary)
