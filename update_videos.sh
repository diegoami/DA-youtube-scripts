#!/bin/bash

update_videos () {
    echo $1
    echo $2

    rm youtube-scripts/update_videos_in_dir.py-oauth2.json
    python youtube-scripts/update_videos_in_dir.py --workDir youtube-scripts/$1/ --outDir /media/diego/Data/musicvideos/$1/
}

echo "Example : update_videos.sh /media/diego/Data/musicvideos"

update_videos 'italian' $1
update_videos 'russian' $1
update_videos 'polish' $1
update_videos 'southslavic' $1
update_videos 'romanian' $1
update_videos 'french' $1
update_videos 'easteurope' $1
