#!/bin/bash

update_liked () {
    echo $1

    rm youtube-scripts/save_liked_videos.py-oauth2.json
    rm youtube.dat
    python youtube-scripts/save_liked_videos.py --workDir $2/$1
}

echo "Example : update_liked.sh youtube-scripts"
ARG1=${1:-youtube-scripts}
echo $ARG1
update_liked 'italian' $ARG1
update_liked 'russian' $ARG1
update_liked 'polish' $ARG1
update_liked 'southslavic' $ARG1
update_liked 'romanian' $ARG1
update_liked 'french' $ARG1
update_liked 'easteurope' $ARG1
#update_liked 'techcontroversy' $1
