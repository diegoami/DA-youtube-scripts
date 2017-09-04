from oauth2client.tools import argparser

import glob
import os
import itertools
import subprocess as sp

def conv_to_audio(inputFile, outputFile):
    clip = mp.VideoFileClip(inputFile)
    clip.audio.write_audiofile(outputFile)

def conv_to_flac(inputFile, outputFile):
    cmd= [ "ffmpeg", '-i',inputFile, "-ac", "1" , outputFile]
    newprocess = sp.Popen(cmd)
    newprocess.wait()


if __name__ == "__main__":
    import moviepy.editor as mp

    argparser.add_argument('--inputDir')
    argparser.add_argument('--outputDir')

    args = argparser.parse_args()

    filenames1 = list(glob.iglob(args.inputDir + '/*.mp4'))
    filenames2 = list(glob.iglob(args.inputDir + '/*.webm'))
    filenames3 = list(glob.iglob(args.inputDir + '/*.mkv'))
    filenames = filenames1 + filenames2 + filenames3
    for filename in filenames:
        print(filename)
        basename = os.path.basename(filename)
        file_root, file_extension = os.path.splitext(basename )
        #print(file_root)
        ouputaudiofile = args.outputDir+'/'+file_root+".mp3"
        ouputaudiofileFlac = args.outputDir + '/' + file_root + ".flac"

        if not os.path.isfile(ouputaudiofile):
            print("Saving {}".format(ouputaudiofile))
            try:
                conv_to_audio(filename, ouputaudiofile )
            except:
                print("Error converting {}".format(ouputaudiofile))

        else:
            print("Skipping {}".format(ouputaudiofile))
        if False and not os.path.isfile(ouputaudiofileFlac):
            print("Saving {}".format(ouputaudiofileFlac))
            try:
                conv_to_flac(ouputaudiofile, ouputaudiofileFlac)
            except:
                print("Error converting {}".format(ouputaudiofileFlac))
        else:
            print("Skipping {}".format(ouputaudiofileFlac))


            #conv_to_audio(args.inputDir or "", args.inputFile, args.outputFile)

