from youtube3 import YoutubeClient
from oauth2client.tools import argparser
import os
if __name__ == "__main__":
    argparser.add_argument('--videoId')
    args = argparser.parse_args()
    if args.videoId == None:
        print("required argument --videoId <videoId>")
    else:
        youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
        videoInfo = youtube_client .get_video(args.videoId )
        channelId = youtube_client .get_channel_id(args.videoId )
        relatedVideos = youtube_client .get_related_videos(args.videoId )
        print(videoInfo)
        print(channelId)
        print(relatedVideos)