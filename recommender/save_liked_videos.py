from youtube3.youtube import *
import json
from oauth2client.tools import argparser
import os.path
if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--maxCount')
    args = argparser.parse_args()
    youtube = Youtube(get_authenticated_service(args))
    maxCount = args.maxCount or 2000
    likedchannel  = youtube.liked_channel()
    print(likedchannel)

    count = 0
    liked = {}
    if os.path.isfile(args.workDir+'/liked.json'):
        with open(args.workDir+'/liked.json','r',encoding="utf-8") as f:
            liked = json.load(f)


    for videos in youtube.iterate_videos_in_channel(likedchannel,maxCount):
        for item in videos['items']:
            print(item['contentDetails']['videoId'],item['snippet']['title'])
            liked[item['contentDetails']['videoId']] = item['snippet']['title']
        count = count + 1

    with open(args.workDir+'/liked.json','w',encoding="utf-8") as f:
        json.dump(liked,f,ensure_ascii=False )
