#!/bin/bash

update_videos () {
    echo $1
    echo $2

    rm youtube-scripts/save_liked_videos.py-oauth2.json
    rm youtube-scripts/download_videos.py-oauth2.json

    python youtube-scripts/save_liked_videos.py --workDir youtube-scripts/$1/
    python youtube-scripts/download_videos.py --workDir youtube-scripts/$1 --inputFile liked.json --outDir /media/diego/Data/musicvideos/$1/
}

echo "Example : update_videos.sh /media/diego/Data/musicvideos"

update_videos 'italian' $1
update_videos 'russian' $1
update_videos 'polish' $1
update_videos 'southslavic' $1
update_videos 'romanian' $1
update_videos 'french' $1
update_videos 'easteurope' $1
