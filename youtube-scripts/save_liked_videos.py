from youtube3 import YoutubeClient
import json
from oauth2client.tools import argparser
import os.path
import sys


def save_video_list(youtube, max_count, work_dir, channel_id):

    channel_file = None
    if (channel_id is None):
        channel_id = youtube.liked_channel()
        output_file = work_dir+'/liked.json'
        channel_file = work_dir +'/channels.json'
    else:
        channel_id = channel_id
        output_file = work_dir + '/'+ channel_id +'.json'

    channels = {}
    print("Saving video descriptions from the channel {} into the file {} ".format(channel_id, output_file))
    count = 0
    liked = {}
    if os.path.isfile(output_file):
        with open(output_file, 'r', encoding="utf-8") as f:
            liked = json.load(f)
    if channel_file and os.path.isfile(channel_file):
        with open(output_file, 'r', encoding="utf-8") as f:
            channels = json.load(channel_file)
    for videos in youtube.iterate_videos_in_channel(channel_id, max_count):
        for item in videos['items']:
            video_id = item['contentDetails']['videoId']
            print(item['contentDetails']['videoId'], item['snippet']['title'])
            liked[item['contentDetails']['videoId']] = item['snippet']['title']

        count = count + 1
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(liked, f, ensure_ascii=False)

if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--maxCount')
    argparser.add_argument('--channelId')

    args = argparser.parse_args()
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    maxCount = args.maxCount or 2000
    if (args.workDir is None):
        print("Usage : python save_liked_videos.py --workdDir <workDir> --maxCount <maxCount> --channelId <channelId>")
        sys.exit(0)

    if not os.path.isdir(args.workDir):
        print("{} does not exist -- exiting".format(args.workDir))
        sys.exit(0)


    save_video_list(youtube=youtube_client, max_count=maxCount, work_dir=args.workDir, channel_id=args.channelId)
