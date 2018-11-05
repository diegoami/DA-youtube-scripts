#!/bin/bash

update_liked () {
    echo $1

    rm youtube-scripts/save_liked_videos.py-oauth2.json
    python youtube-scripts/save_liked_videos.py --workDir $2/$1
}

echo "Example : update_liked.sh youtube-scripts"

update_liked 'italian' $1
update_liked 'russian' $1
update_liked 'polish' $1
update_liked 'southslavic' $1
update_liked 'romanian' $1
update_liked 'french' $1
update_liked 'easteurope' $1
#update_liked 'techcontroversy' $1
