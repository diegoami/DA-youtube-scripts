from oauth2client.tools import argparser

def conv_to_audio(inputDir, inputFile, outputFile):
    clip = mp.VideoFileClip(inputDir+inputFile)
    clip.audio.write_audiofile(outputFile)

if __name__ == "__main__":
    import moviepy.editor as mp

    argparser.add_argument('--inputDir')
    argparser.add_argument('--inputFile')
    argparser.add_argument('--outputFile')

    args = argparser.parse_args()
    conv_to_audio(args.inputDir or "", args.inputFile, args.outputFile)