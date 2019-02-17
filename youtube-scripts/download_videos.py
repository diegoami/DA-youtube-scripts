import os
from youtube3 import YoutubeClient
import json
import shutil
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL
from oauth2client.tools import argparser
import traceback
from youtube_dl.utils import sanitize_filename
import sys
import fnmatch
import os
from blogspotapi import BlogRepository, BlogPost


def download_videos(youtube, blog_repository, out_dir, with_subtitles=False):

    for post_id, blog_post in blog_repository.posts_map.items():
        video_id = blog_post.videoId
        title = blog_post.title
        try:
            channel_id = youtube.get_channel_id(video_id)
            channel_name = youtube.get_channel_name(channel_id)

            channel_dir_title = out_dir + channel_id+'_'+sanitize_filename(channel_name)


            if os.path.exists(channel_dir_title):
                pass
            else:
                print("Creating directory {}".format(channel_dir_title))
                os.mkdir(channel_dir_title)

            files_in_chan_dir = os.listdir(channel_dir_title)
            psb_regexp = '*-' + video_id + '.*'

            matching_in_channel = fnmatch.filter(files_in_chan_dir, psb_regexp)

            if len(matching_in_channel) > 0:
                print("Found {} in {}, passing".format(video_id, channel_dir_title))
                pass
            else:
                print("Must download {}".format(video_id, channel_dir_title))
                print("Trying to start process to download {} {}".format(video_id, channel_dir_title))
                url = "http://www.youtube.com/watch?v=" + video_id

                with YoutubeDL({'format': 'best', 'merge-output-format': 'mp4', 'cachedir': False,
                                    'outtmpl': channel_dir_title + '/' +DEFAULT_OUTTMPL, "nooverwrites": True}) as youtube_dl:
                    youtube_dl.download([url])
            if with_subtitles:

                matching_in_channel = fnmatch.filter(files_in_chan_dir, psb_regexp)
                if len(matching_in_channel) > 0:
                    matching_file = matching_in_channel[0]
                    srt_file = os.path.splitext(matching_file)[0]+'.srt'
                    if os.path.isfile(srt_file):
                        print("Skipping already saved subtitles for {} in {}, passing".format(video_id, channel_dir_title))
                    else:
                        sub_titles = blog_repository.get_subtitles_for(video_id)
                        if sub_titles:
                            print("Saving subtitles for {} to file {}".format(video_id, srt_file))
                            with open(os.path.join(channel_dir_title, srt_file), 'w') as f:
                                f.writelines(sub_titles)
                        else:
                            print("No subtitles exist for {}, ".format(video_id, matching_file))
        except:
            print("Skipping {} : {}".format(video_id, title))
            traceback.print_exc(file=sys.stdout)

    for channel_id in youtube.channel_snippet_map:
        channel_dir_id = out_dir + channel_id
        if os.path.exists(channel_dir_id):
            print("Removing directory {}".format(channel_dir_id))
            shutil.rmtree(channel_dir_id)


if __name__ == "__main__":
    argparser.add_argument('--blogId')
    argparser.add_argument('--outDir')
    argparser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    argparser.add_argument('--with_subtitles', dest='with_subtitles', action='store_true')
    argparser.add_argument('--no-with_subtitles', dest='with_subtitles', action='store_false')
    argparser.set_defaults(with_subtitles=True)
    args = argparser.parse_args()

    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    blog_repository = BlogRepository(args.mongo_connection, args.blogId)

    if (args.outDir is None):
        print("Usage : python download_videos.py --outDir <outputDirectory> --blogId <blogSource> ")
        sys.exit(0)

    if not os.path.isdir(args.outDir):
        print("{} does not exist -- creating it".format(args.outDir))
        os.mkdir(args.outDir)

    download_videos(youtube_client, blog_repository, out_dir=args.outDir, with_subtitles=args.with_subtitles)
