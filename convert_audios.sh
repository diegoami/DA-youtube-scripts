#!/usr/bin/env bash




convert_audios () {
    echo $1
    python youtube-scripts/convert_to_audios.py --inputDir /home/diego/musicvideos/$1 --outDir /home/diego/musicaudios/$1
}

convert_audios 'italian'
convert_audios 'russian'
convert_audios 'polish'
convert_audios 'southslavic'
convert_audios 'romanian'
convert_audios 'french'
convert_audios 'easteurope'
