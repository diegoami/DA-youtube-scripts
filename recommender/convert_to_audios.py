from oauth2client.tools import argparser

import glob
import os
import itertools

def conv_to_audio(inputFile, outputFile):
    clip = mp.VideoFileClip(inputFile)
    clip.audio.write_audiofile(outputFile)


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
        conv_to_audio(filename, ouputaudiofile )
    #conv_to_audio(args.inputDir or "", args.inputFile, args.outputFile)

