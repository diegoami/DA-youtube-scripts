from youtube3.youtube import *
import json
from oauth2client.tools import argparser
import re


def load_definition(records, inputFile, workDir):
    if os.path.isfile(workDir + '/' + inputFile):
        with open(workDir + '/' + inputFile, 'r', encoding="utf-8") as f:
            records = dict(json.load(f))
    return records



if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--inputFile')
    argparser.add_argument('--start')
    argparser.add_argument('--end')
    argparser.add_argument('--outDir')

    args = argparser.parse_args()
    videos_json = {}
    videos_json = load_definition(videos_json, args.inputFile, args.workDir)
    video_key_lst = [k for k, v in videos_json.items()]
    start = int(args.start) if args.start else 0
    end = min(int(args.end), len(video_key_lst)) if args.end else len(video_key_lst)
    donwload_list = video_key_lst[start:end]

    youtube = Youtube(get_authenticated_service(args))
    youtube.download_list(donwload_list, args.outDir)
