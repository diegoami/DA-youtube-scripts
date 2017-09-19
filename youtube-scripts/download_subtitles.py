from amaraapi.amara import Amara

import sys
sys.path.append('..')

import argparse
from amara_env import amara_headers
import os
import json
import traceback
def load_definition(records, inputFile, workDir):
    inputFileC = workDir + '/' + inputFile
    if os.path.isfile(inputFileC):
        with open(inputFileC, 'r', encoding="utf-8") as f:
            records = dict(json.load(f))
    else:
        print("Cannot find file {}".format(inputFileC))
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


    if (args.workDir is None or args.inputFile is None or args.outDir is None):
        print("Usage : python download_subtitles.py --workDir <workDir> --inputFile <inputFile> --outDir <outDir>")
        sys.exit(0)

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
            title = videos_json[to_download]
            title = title.replace('/','_')
            title = title.replace('|', '_')

            file_name = args.outDir+'/'+title+'-'+to_download+'.srt'


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
            traceback.print_exc(file=sys.stdout)