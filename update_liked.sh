#!/bin/bash

update_liked () {
    echo $1

    rm youtube-scripts/save_liked_videos.py-oauth2.json
    python youtube-scripts/save_liked_videos.py --workDir youtube-scripts/$1/
}

echo "Example : update_videos.sh /media/diego/Data/musicvideos"

update_liked 'italian' $1
update_liked 'russian' $1
update_liked 'polish' $1
update_liked 'southslavic' $1
update_liked 'romanian' $1
update_liked 'french' $1
update_liked 'easteurope' $1
