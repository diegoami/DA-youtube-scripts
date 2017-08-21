from amaraapi.amara import Amara

import argparse
from amara_env import amara_headers
import os
import json

def load_definition(records, inputFile, workDir):
    if os.path.isfile(workDir + '/' + inputFile):
        with open(workDir + '/' + inputFile, 'r', encoding="utf-8") as f:
            records = dict(json.load(f))
    return records



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--workDir')
    argparser.add_argument('--inputFile')
    argparser.add_argument('--start')
    argparser.add_argument('--end')
    argparser.add_argument('--outDir')
    argparser.add_argument('--language')

    args = argparser.parse_args()

    amara = Amara(amara_headers)
    args = argparser.parse_args()
    videos_json = {}
    videos_json = load_definition(videos_json, args.inputFile, args.workDir)
    video_key_lst = [k for k, v in videos_json.items()]
    start = int(args.start) if args.start else 0
    end = min(int(args.end), len(video_key_lst)) if args.end else len(video_key_lst)
    download_list = video_key_lst[start:end]
    amara = Amara(amara_headers)
    for to_download in download_list:
        try:
            file_name = args.outDir+'/'+videos_json[to_download]+'-'+to_download+'.srt'
            if not os.path.isfile(file_name ):
                amara_video = amara.retrieve_video(to_download)
                if (amara_video):
                    subtitles = amara_video.get_best_subtitles()
                    if (subtitles):
                        with open(file_name, 'w', encoding="utf-8") as f:
                            print("Writing subtitles to {}".format(file_name))
                            f.writelines(subtitles)
                    else:
                        print("No valid subtitles: Skipping {}".format(to_download))
                else:
                    print("No video on Amara: Skipping {}".format(to_download))
            else:
                print("File exists: {}".format(file_name))


        except:
            print("Error : Skipping {}".format(to_download))