import os
from youtube3.youtube import *
import json
from oauth2client.tools import argparser
import traceback
from youtube_dl.utils import sanitize_filename
import sys



def load_definition(records, inputFile, workDir):
    inputFileC = workDir + '/' + inputFile
    if os.path.isfile(inputFileC):
        with open(inputFileC, 'r', encoding="utf-8") as f:
            records = dict(json.load(f))
    else:
        print("Cannot find file {}".format(inputFileC))
    return records



if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--inputFile')
    argparser.add_argument('--start')
    argparser.add_argument('--end')
    argparser.add_argument('--outDir')

    args = argparser.parse_args()
    videos_json = {}
    if (args.workDir is None or args.inputFile is None or args.outDir is None):
        print("Usage : python download_videos.py --workdDir <workDir> --inputFile <inputFile> --outDir <outputDirectory>  ")
        sys.exit(0)

    if not os.path.isdir(args.outDir):
        print("{} does not exist -- exiting".format(args.outDir))
        sys.exit(0)

    if not os.path.isdir(args.workDir):
        print("{} does not exist -- exiting".format(args.workDir))
        sys.exit(0)

    videos_json = load_definition(videos_json, args.inputFile, args.workDir)
    video_key_lst = [k for k, v in videos_json.items()]
    start = int(args.start) if args.start else 0
    end = min(int(args.end), len(video_key_lst)) if args.end else len(video_key_lst)
    download_list = video_key_lst[start:end]
    youtube = Youtube(get_authenticated_service(args))
    for to_download in download_list:
        try:
            title = videos_json[to_download]

            file_name_main = args.outDir + '/' + sanitize_filename(title) + '-' + to_download
            psb_filenames = [file_name_main+'.' + ext for ext in ['webm', 'mkv','mp4']]
            if any([ os.path.isfile(psb_filename) for psb_filename  in psb_filenames ]):
                print("Found file {}, skipping".format(file_name_main ))
                continue

            youtube.download(to_download, args.outDir)
        except:
            print("Skipping {}".format(to_download))
            traceback.print_exc(file=sys.stdout)
