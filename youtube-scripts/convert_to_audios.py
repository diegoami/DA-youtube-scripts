from oauth2client.tools import argparser
import traceback
import glob
import os
import itertools
import sys
import subprocess as sp
import moviepy.editor as mp

def conv_to_audio(inputFile, outputFile):
    clip = mp.VideoFileClip(inputFile)
    clip.audio.write_audiofile(outputFile)

def conv_to_audio_gen(inputFile, outputFile):
    cmd= [ "ffmpeg", '-i',inputFile, "-ac", "1" , outputFile]
    newprocess = sp.Popen(cmd)
    newprocess.wait()


if __name__ == "__main__":


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


    filenames = list(glob.iglob(args.inputDir + '/**/*.mp4', recursive=True))

    for filename in filenames:
        print(filename)
    basename = os.path.basename(filename)
    file_root, file_extension = os.path.splitext(basename )
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




