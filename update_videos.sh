#!/bin/bash

update_videos () {
    echo $1
    echo $2
    echo $3
    pushd youtube-scripts
    python download_videos.py --blogId $1 --outDir $3/$2/
    popd
}

echo "Example : update_videos.sh /media/diego/Data/musicvideos"

update_videos 6377950492326759990 'italian' $1
update_videos 446998987295244185 'russian' $1
update_videos 59695003203290655 'polish' $1
update_videos 556901760723185848 'southslavic' $1
update_videos 8277328596134486858 'romanian' $1
update_videos 2775451793153626665 'french' $1
update_videos 4061164319975225752 'easteurope' $1
