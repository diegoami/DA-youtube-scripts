from youtube3.youtube import *
import json
from oauth2client.tools import argparser
import re


def process_videos(workDir='.', inputFile='liked.json', recommendedFile='recommended.json',
                   excludedFile='excluded.json', postponedFile='postponed.json',maxCount=5):


    recommended, excluded, postponed, liked = {}, {}, {}, {}
    workDir, inputFile, recommendedFile, excludedFile, postponedFile = workDir or '.', inputFile or 'liked.json', \
             recommendedFile or 'recommended.json', excludedFile or 'excluded.json', postponedFile or 'postponed.json'

    liked = load_definition(liked, inputFile, workDir)
    recommended = load_definition(recommended, recommendedFile, workDir)
    excluded = load_definition(excluded, excludedFile, workDir)
    postponed = load_definition(postponed, postponedFile, args.workDir)
    start = int(args.start) if args.start else 0
    end = min(int(args.end), len(liked)) if args.end else len(liked)
    youtube = Youtube(get_authenticated_service(args))
    likedList = list(liked.items())[start:end]
    for videoId, title in likedList:
        print("Now processing %s, %s" % (videoId, title))
        for relatedvideos in youtube.iterate_related_videos(videoId, maxCount):
            for item in relatedvideos['items']:
                rvideoId, rtitle = item['id']['videoId'], item['snippet']['title']
                if rvideoId not in liked and rvideoId not in excluded and rvideoId not in postponed:
                    if rvideoId not in recommended:
                        recommended[rvideoId] = {"title": rtitle, "count": 1}
                    else:
                        recommended[rvideoId]["count"] += 1
    recommendedSorted = sorted(recommended.items(), key=lambda x: x[1]["count"], reverse=True)
    return recommendedSorted


def load_definition(records, inputFile, workDir):
    inputFileC = workDir + '/' + inputFile
    if os.path.isfile(inputFileC):
        with open(inputFileC, 'r', encoding="utf-8") as f:
            records = dict(json.load(f))
    else:
        print("Cannot find file {}".format(inputFileC))
    return records


def tokenize_lists( recommended, liked, workDir , ignore_words_file):

    def get_tokenized(str,ignored_words):
        str = str.lower()
        str = re.sub(r"\(.*\)", "" , str)
        str = re.sub(r"[0-9]+", "", str)

        strtok = re.split(r'[\[\s\-\(\)\"\\\/\|\!\&\,\.\+]',str)
        strl = [s for s in strtok if s not in ignored_words and len(s) > 0]
        return strl

    ignored_words = []
    if os.path.isfile(workDir + '/' + ignore_words_file):
        with open(workDir + '/' + ignore_words_file, 'r', encoding="utf-8") as f:
            ignored_words = f.read().splitlines()
    ignored_words = [ i.lower() for i in ignored_words]
    tok_liked = {k:get_tokenized(v,ignored_words) for k,v in liked.items()}
    tok_liked_list = [get_tokenized(v, ignored_words) for k, v in liked.items()]
    #print(tok_liked_list)
    tok_recommended = {k: {"title": get_tokenized(v["title"],ignored_words), "count": v["count"]}  for k, v in recommended.items()}
    tok_duplicates = {k: {"title": v["title"], "count": v["count"]} for k, v in
                      tok_recommended.items() if v["title"] in tok_liked_list}
    tok_no_duplicates = {k: {"title": v["title"], "count": v["count"]} for k, v in
                         tok_recommended.items() if v["title"] not in tok_liked_list}
    return tok_duplicates, tok_no_duplicates


def save_recommended(workDir='.', recommendedFile='recommended.json', recommendedSorted={}  ):
    workDir, recommendedFile, recommendedSorted = workDir or '.', \
             recommendedFile or 'recommended.json', recommendedSorted or {}
    save_to_json(recommendedFile, recommendedSorted, workDir)


def save_to_json(outputFile, outputData, workDir):

    with open(workDir + '/' + outputFile, 'w', encoding="utf-8") as f:
        json.dump(outputData, f, ensure_ascii=False)
        print("Saved file: {}".format(workDir + '/' + outputFile))


def retrieve_recommended(args):
    recommendedSorted = process_videos(workDir=args.workDir, inputFile=args.inputFile,
                                       recommendedFile=args.recommendedFile,
                                       excludedFile=args.excludedFile, postponedFile=args.postponedFile,
                                       maxCount=args.maxCount)
    save_recommended(workDir=args.workDir, recommendedFile=args.recommendedFile, recommendedSorted=recommendedSorted)
    return recommendedSorted


def eliminate_duplicates(args):
    liked, recommended = {}, {}


    liked = load_definition(liked, args.inputFile, args.workDir)
    recommended = load_definition(recommended, args.recommendedFile or 'recommended.json', args.workDir)
    duplicates, no_duplicates = tokenize_lists(recommended=recommended, liked=liked, workDir=args.workDir,
                                               ignore_words_file='ignore_words.txt')
    save_to_json(outputData=list([[k, v] for k, v in duplicates.items()]), outputFile='duplicates.json',
                 workDir=args.workDir)
    save_to_json(outputData=list([[k, v] for k, v in no_duplicates.items()]), outputFile='recommended_no_dup.json',
                 workDir=args.workDir)


if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--maxCount')
    argparser.add_argument('--inputFile')


    argparser.add_argument('--start')
    argparser.add_argument('--end')
    argparser.add_argument('--recommendedFile')
    argparser.add_argument('--excludedFile')
    argparser.add_argument('--postponedFile')


    args = argparser.parse_args()

    if (args.workDir is None):
        print("Usage : python recommend_videos.py --workdDir <workDir> --maxCount <maxCount> --inputFile <file>")
        sys.exit(0)

    if not os.path.isdir(args.workDir):
        print("{} does not exist -- exiting".format(args.workDir))
        sys.exit(0)

    retrieve_recommended(args)
    eliminate_duplicates(args)
