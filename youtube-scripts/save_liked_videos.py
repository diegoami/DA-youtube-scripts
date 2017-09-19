from youtube3.youtube import *
import json
from oauth2client.tools import argparser
import os.path
import sys
if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--maxCount')
    args = argparser.parse_args()
    youtube = Youtube(get_authenticated_service(args))
    maxCount = args.maxCount or 2000
    if (args.workDir is None):
        print("Usage : python save_liked_videos.py --workdDir <workDir> --maxCount <maxCount>")
        sys.exit(0)

    if not os.path.isdir(args.workDir):
        print("{} does not exist -- exiting".format(args.workDir))
        sys.exit(0)

    likedchannel = youtube.liked_channel()
    outputFile = args.workDir+'/liked.json'
    print("Saving video descriptions from the channel {} into the file {} ".format(likedchannel, outputFile ))

    count = 0
    liked = {}
    if os.path.isfile(outputFile ):
        with open(outputFile, 'r',encoding="utf-8") as f:
            liked = json.load(f)


    for videos in youtube.iterate_videos_in_channel(likedchannel,maxCount):
        for item in videos['items']:
            print(item['contentDetails']['videoId'],item['snippet']['title'])
            liked[item['contentDetails']['videoId']] = item['snippet']['title']
        count = count + 1

    with open(outputFile, 'w',encoding="utf-8") as f:
        json.dump(liked,f,ensure_ascii=False )
