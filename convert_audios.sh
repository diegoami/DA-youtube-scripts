#!/usr/bin/env bash




convert_audios () {
    echo $1
    python youtube-scripts/convert_to_audios.py --inputDir $2/musicvideos/$1 --outDir $2/musicaudios/$1
}

echo "Example : convert_audios.sh /media/diego/Samsung_T5"


convert_audios 'italian' $1
convert_audios 'russian' $1
convert_audios 'polish' $1
convert_audios 'southslavic' $1
convert_audios 'romanian' $1
convert_audios 'french' $1
convert_audios 'easteurope' $1
