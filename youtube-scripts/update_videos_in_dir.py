from youtube3.youtube import *
from oauth2client.tools import argparser
import sys


from save_liked_videos import save_video_list
from download_videos import download_videos





if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--channelId')
    argparser.add_argument('--maxCount')
    argparser.add_argument('--outDir')
    argparser.add_argument('--origDir')

    args = argparser.parse_args()

    if (args.workDir is None):
        print("Usage : python update_videos.py --workdDir <workDir> --maxCount <maxCount> --channelId <channelId> --outDir <outDir> --origDir <origDir>" )
        sys.exit(0)

    maxCount = args.maxCount or 2000

    youtube = Youtube(get_authenticated_service(args))


    save_video_list(youtube=youtube, max_count=maxCount,  work_dir=args.workDir, channel_id=args.channelId)
    download_videos(youtube=youtube, input_file='liked.json', work_dir=args.workDir, start=None, end=None, out_dir=args.outDir, orig_dir=args.origDir)

