import os
from youtube3.youtube import *
import json
from oauth2client.tools import argparser
import traceback
from youtube_dl.utils import sanitize_filename
import sys
import fnmatch
import os
import shutil



def load_definition(inputFile, workDir):
    records = {}
    if inputFile:
        inputFileC = workDir + '/' + inputFile
        if os.path.isfile(inputFileC):
            with open(inputFileC, 'r', encoding="utf-8") as f:
                records = dict(json.load(f))
        else:
            print("Cannot find file {}".format(inputFileC))
            records = {}
    return records


def download_videos(youtube, input_file, work_dir, start, end, out_dir, orig_dir=None):

    videos_json = load_definition(input_file, work_dir)

    video_key_lst = [k for k, v in videos_json.items()]
    start = int(start) if start else 0
    end = min(int(end), len(video_key_lst)) if end else len(video_key_lst)
    download_list = video_key_lst[start:end]
    files_in_main_dir = os.listdir(out_dir)
    subscriptions = list(youtube.iterate_subscriptions_in_channel())
    submap = {s['id'] : s['title'] for s in subscriptions}

    for video_id in download_list:
        try:
            title = videos_json[video_id]
            channel_id = youtube.get_channel_id(video_id)
            if channel_id in submap:
                channel_name = submap[channel_id]
            else:
                channel_name = youtube.get_channel_title(channel_id)


            channel_dir = out_dir + channel_id
            channel_dir_title = out_dir + channel_id+'_'+sanitize_filename(channel_name)
            if (orig_dir):
                orig_dir_title = orig_dir + channel_id+'_'+sanitize_filename(channel_name)
            else:
                orig_dir_title = None

            if os.path.exists(channel_dir_title ):

                pass
            elif os.path.exists(channel_dir ):
                print("Renaming dir {} to {} ".format(channel_dir , channel_dir_title ))
                os.rename(channel_dir, channel_dir_title)
            else:
                print("Creating directory {}".format(channel_dir_title))
                os.mkdir(channel_dir_title)

            files_in_chan_dir = os.listdir(channel_dir_title)
            psb_regexp = '*-' + video_id + '.*'

            matching_in_main = fnmatch.filter(files_in_main_dir, psb_regexp )
            matching_in_channel = fnmatch.filter(files_in_chan_dir, psb_regexp )


            if len(matching_in_main) > 0:
                for file_matching in matching_in_main:
                    print("Moving file {} from {} to {} ".format(file_matching, out_dir, channel_dir))
                    os.rename(out_dir+'/'+ file_matching , channel_dir + '/'+ file_matching )
            elif len(matching_in_channel) > 0:
                print("Found {} in {}, passing".format(video_id, channel_dir_title))
                pass
            else:
                if orig_dir_title:
                    files_in_orig_dir = os.listdir(orig_dir_title)
                    matching_in_orig = fnmatch.filter(files_in_orig_dir, psb_regexp)
                    if len(matching_in_orig) > 0:
                        for file_matching in matching_in_orig:
                            shutil.copy(orig_dir_title+'/'+ file_matching , channel_dir_title + '/' + file_matching )
                            print("Coping {} from {} to {} ".format(file_matching, orig_dir_title, channel_dir_title))
                else:
                    youtube.download(video_id, channel_dir_title )
                    print("Downloading {} to {} ".format(video_id, channel_dir_title))

        except:
            print("Skipping {} : {}".format(video_id, title))
            traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--inputFile')
    argparser.add_argument('--start')
    argparser.add_argument('--end')
    argparser.add_argument('--outDir')
    argparser.add_argument('--origDir')

    args = argparser.parse_args()
    youtube = Youtube(get_authenticated_service(args))
    if (args.workDir is None or args.inputFile is None or args.outDir is None):
        print("Usage : python download_videos.py --workdDir <workDir> --inputFile <inputFile> --outDir <outputDirectory> --origDir <originalDirectory> ")
        sys.exit(0)

    if not os.path.isdir(args.outDir):
        print("{} does not exist -- exiting".format(args.outDir))
        sys.exit(0)

    if not os.path.isdir(args.workDir):
        print("{} does not exist -- exiting".format(args.workDir))
        sys.exit(0)

    download_videos(youtube, input_file=args.inputFile, work_dir=args.workDir,start=args.start, end=args.end, out_dir=args.outDir, orig_dir=args.origDir)
