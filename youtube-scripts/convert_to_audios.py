from oauth2client.tools import argparser
import traceback
import glob
import os
import itertools
import sys
import subprocess as sp


def conv_to_audio(inputFile, outputFile):
    clip = mp.VideoFileClip(inputFile)
    clip.audio.write_audiofile(outputFile)

def conv_to_audio_gen(inputFile, outputFile):
    cmd= [ "ffmpeg", '-i',inputFile, "-ac", "1" , outputFile]
    newprocess = sp.Popen(cmd)
    newprocess.wait()


if __name__ == "__main__":
    import moviepy.editor as mp

    argparser.add_argument('--inputDir')
    argparser.add_argument('--outDir')

    args = argparser.parse_args()
    if (args.inputDir is None or args.outDir is None ) :
        print("Usage : python convert_to_audios.py --inputDir <inputDir> --outDir <outDir>")
        sys.exit(0)

    if not os.path.isdir(args.inputDir):
        print("{} does not exist -- exiting".format(args.inputDir))
        sys.exit(0)

    if not os.path.isdir(args.outDir):
        print("{} does not exist -- exiting".format(args.outDir))
        sys.exit(0)


    filenames1 = list(glob.iglob(args.inputDir + '/**/*.mp4', recursive=True))
    filenames2 = list(glob.iglob(args.inputDir + '/**/*.webm', recursive=True))
    filenames3 = list(glob.iglob(args.inputDir + '/**/*.mkv', recursive=True))
    filenames = filenames1 + filenames2 + filenames3
    for filename in filenames:
        print(filename)

        basename = os.path.basename(filename)

        file_root, file_extension = os.path.splitext(basename )
        subtitle_file = args.inputDir+'/'+file_root+".srt"
        ouputaudiofile = args.outDir+'/'+file_root+".mp3"

        if not os.path.isfile(ouputaudiofile) :
            print("Saving {}".format(ouputaudiofile))
            try:
                conv_to_audio(filename, ouputaudiofile )
            except:
                print("Error converting {}".format(ouputaudiofile))

                traceback.print_exc(file=sys.stdout)
        else:
            print("Skipping {}".format(ouputaudiofile))


            #conv_to_audio(args.inputDir or "", args.inputFile, args.outputFile)

