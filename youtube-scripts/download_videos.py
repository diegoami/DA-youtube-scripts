import os
from youtube3 import YoutubeClient
import json

from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL
from oauth2client.tools import argparser
import traceback
from youtube_dl.utils import sanitize_filename
import sys
import fnmatch
import os
from blogspotapi import BlogRepository, BlogPost


def download_videos(youtube, blog_repository, out_dir, orig_dir=None):
    channel_map = {}
    for post_id, blog_post in blog_repository.posts_map.items():
        video_id = blog_post.videoId
        title = blog_post.title
        try:
            channel_id = youtube.get_channel_id(video_id)
            print("Processing {} in channel {}".format(title, channel_id))
            if channel_id in channel_map:
                channel_name = channel_map[channel_id]
            else:
                channel_name = youtube.get_channel_title(channel_id)

            channel_dir_title = out_dir + channel_id+'_'+sanitize_filename(channel_name)

            if os.path.exists(channel_dir_title):
                pass
            else:
                print("Creating directory {}".format(channel_dir_title))
                os.mkdir(channel_dir_title)

            files_in_chan_dir = os.listdir(channel_dir_title)
            psb_regexp = '*-' + video_id + '.*'

            matching_in_channel = fnmatch.filter(files_in_chan_dir, psb_regexp )

            if len(matching_in_channel) > 0:
                print("Found {} in {}, passing".format(video_id, channel_dir_title))
                pass
            else:
                print("Must download {}".format(video_id, channel_dir_title))
                print("Trying to start process to download {} {}".format(video_id, channel_dir_title))
                url = "http://www.youtube.com/watch?v=" + video_id

                with YoutubeDL({'format': 'best', 'merge-output-format': 'mp4',
                                    'outtmpl': channel_dir_title + '/' +DEFAULT_OUTTMPL, "nooverwrites": True}) as youtube_dl:
                    youtube_dl.download([url])
        except:
                print("Skipping {} : {}".format(video_id, title))
                traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    argparser.add_argument('--blogId')
    argparser.add_argument('--outDir')
    argparser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    args = argparser.parse_args()

    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    blog_repository = BlogRepository(args.mongo_connection, args.blogId)

    if (args.outDir is None):
        print("Usage : python download_videos.py --outDir <outputDirectory> --blogId <blogSource> ")
        sys.exit(0)

    if not os.path.isdir(args.outDir):
        print("{} does not exist -- creating it".format(args.outDir))
        os.mkdir(args.outDir)

    download_videos(youtube_client, blog_repository, out_dir=args.outDir)
